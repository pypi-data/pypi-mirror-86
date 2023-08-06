"""
Utility to match peaks from results of different processor versions / processor and simulator
Joran Angevaare, october, november 2020
Joey Howlett, February 2020
Joran Angevaare, September 2019
Mike Clark, September 2019
Jelle Aalbers, Nikhef, September 2015
"""

import numpy as np
import pema
import strax
import numba
export, __all__ = strax.exporter()

INT_NAN = -99999
OUTCOME_DTYPE = '<U32'


@export
def match_peaks(allpeaks1, allpeaks2,
                matching_fuzz=0,
                unknown_types=(0,)):
    """
    Perform peak matching between two numpy record arrays with fields:
        Event, left, right, type, area
    If a peak is split into many fragments (e.g. two close peaks split
    into three peaks), the results are unreliable and depend on which
    peak set is peaks1 and which is peaks2.

    Returns (allpeaks1, allpeaks2), each with three extra fields:
    id, outcome, matched_to:
        id: unique number for each peak
        outcome: Can be one of:
            found:  Peak was matched 1-1 between peaks1 and peaks2 (type agrees,
             no other peaks in range).
                    Note that area, widths, etc. can still be quite different!
            missed: Peak is not present in the other list
            misid_as_XX: Peak is present in the other list, but has type XX
            merged: Peak is merged with another peak in the other list, the new
            'super-peak' has the same type
            merged_to_XX: As above, but 'super-peak' has type XX
            split: Peak is split in the other list, but more than one fragment
            has the same type as the parent.
            chopped: As split, but one or several fragments are unclassified,
            exactly one has the correct type.
            split_and_unclassified: As split, but all fragments are unclassified
            in the other list.
            split_and_misid: As split, but at least one fragment has a different
            peak type.
        matched_to: id of matching in *peak* in the other list if outcome is found
        or misid_as_XX, INT_NAN otherwise.
    """
    # Check required fields
    for i, d in enumerate((allpeaks1, allpeaks2)):
        m = ''
        for k in ('area', 'type'):
            if k not in d.dtype.names:
                m += f'Argument {i} misses field {k} required for matching \n'
        if m != '':
            raise ValueError(m)

    # Append id, outcome and matched_to fields
    allpeaks1 = pema.append_fields(
        allpeaks1,
        ('id', 'outcome', 'matched_to'),
        (np.arange(len(allpeaks1)),
         np.array(['missed'] * len(allpeaks1), dtype=OUTCOME_DTYPE),
         INT_NAN * np.ones(len(allpeaks1), dtype=np.int64)))
    allpeaks2 = pema.append_fields(
        allpeaks2,
        ('id', 'outcome', 'matched_to'),
        (np.arange(len(allpeaks2)),
         np.array(['missed'] * len(allpeaks2), dtype=OUTCOME_DTYPE),
         INT_NAN * np.ones(len(allpeaks2), dtype=np.int64)))
    windows = strax.touching_windows(allpeaks1, allpeaks2, window=matching_fuzz)

    # Each of the windows projects to a set of peaks in allpeaks2
    # belonging to allpeaks1. We also need to go the reverse way, which
    # I'm calling deep_windows below.
    deep_windows = np.array(
        [strax.touching_windows(allpeaks2, allpeaks1[l1:r1], window=matching_fuzz)[0]
         if r1 - l1 else [-1, -1]  # placeholder for numba
         for l1, r1 in windows], dtype=(np.int64, np.int64))

    if not len(deep_windows):
        # patch for empty data
        deep_windows = np.array([[-1, -1]], dtype=(np.int64, np.int64))
    assert np.shape(np.shape(deep_windows))[0] == 2, (
        f'deep_windows shape is wrong {np.shape(deep_windows)}\n{deep_windows}')

    # make array for numba
    unknown_types = np.array(unknown_types)

    # Inner matching
    _match_peaks(allpeaks1, allpeaks2, windows, deep_windows, unknown_types)
    return allpeaks1, allpeaks2


@numba.jit(nopython=True, nogil=True, cache=True)
def _match_peaks(allpeaks1, allpeaks2, windows, deep_windows, unknown_types):
    """See match_peaks_strax where we do the functional matching here"""
    # Loop over left and right bounds for peaks 1 by matching to peaks 2
    for peaks_1_i, (l1, r1) in enumerate(windows):
        peaks_1 = allpeaks1[l1:r1]
        if l1 == r1:
            continue

        for p1_i, p1 in enumerate(peaks_1):
            # Matching the other way around using deep_windows
            l2, r2 = deep_windows[peaks_1_i]

            peaks_2 = allpeaks2[l2:r2]
            matching_peaks = peaks_2
            if len(matching_peaks) == 0:
                pass

            elif len(matching_peaks) == 1:
                # A unique match! Hurray!
                p2 = matching_peaks[0]
                p1['matched_to'] = p2['id']
                p2['matched_to'] = p1['id']
                # Do the types match?
                if p1['type'] == p2['type']:
                    p1['outcome'] = 'found'
                    p2['outcome'] = 'found'
                else:
                    if _in(p1['type'], unknown_types):
                        p2['outcome'] = 'unclassified'
                    else:
                        p2['outcome'] = 'misid_as_s' + str(p1['type'])
                    if _in(p2['type'], unknown_types):
                        p1['outcome'] = 'unclassified'
                    else:
                        p1['outcome'] = 'misid_as_s' + str(p2['type'])
                    # If the peaks are unknown in both sets, they will
                    # count as 'found'.
                matching_peaks[0] = p2
            else:
                # More than one peak overlaps p1
                handle_peak_merge(parent=p1,
                                  fragments=matching_peaks,
                                  unknown_types=unknown_types)

            # matching_peaks is a copy, not a view, so we have to copy
            # the results over to peaks_2 manually Sometimes I wish
            # python had references...
            for i_in_matching_peaks, i_in_peaks_2 in enumerate(range(l2, r2)):
                allpeaks2[i_in_peaks_2] = matching_peaks[i_in_matching_peaks]

        # Match in reverse to detect merged peaks >1 peaks in 1 may
        # claim to be matched to a peak in 2, in which case we should
        # correct the outcome...
        for p2_i, p2 in enumerate(peaks_2):
            selection = peaks_1['matched_to'] == p2['id']
            matching_peaks = peaks_1[selection]
            if len(matching_peaks) > 1:
                handle_peak_merge(parent=p2,
                                  fragments=matching_peaks,
                                  unknown_types=unknown_types)

            # matching_peaks is a copy, not a view, so we have to copy
            # the results over to peaks_1 manually Sometimes I wish
            # python had references...
            for i_in_matching_peaks, i_in_peaks_1 in enumerate(
                    np.where(selection)[0]):
                peaks_1[i_in_peaks_1] = matching_peaks[i_in_matching_peaks]


@numba.jit(nopython=True)
def handle_peak_merge(parent, fragments, unknown_types):
    found_types = fragments['type']
    is_ok = found_types == parent['type']
    is_unknown = _in1d(found_types, unknown_types)
    is_misclass = (True ^ is_ok) & (True ^ is_unknown)
    # We have to loop over the fragments to avoid making a copy
    for i in range(len(fragments)):
        if is_unknown[i] or is_misclass[i]:
            if _in(parent['type'], unknown_types):
                fragments[i]['outcome'] = 'merged_to_unknown'
            else:
                fragments[i]['outcome'] = 'merged_to_s' + str(parent['type'])
        else:
            fragments[i]['outcome'] = 'merged'
        # Link the fragments to the parent
        fragments[i]['matched_to'] = parent['id']
    if np.any(is_misclass):
        parent['outcome'] = 'split_and_misid'
    # All fragments are either ok or unknown. If more than one fragment
    # is given the same class as the parent peak, then call it "split".
    elif len(np.where(is_ok)[0]) > 1:
        parent['outcome'] = 'split'
    elif np.all(is_unknown):
        parent['outcome'] = 'split_and_unclassified'
    # If exactly one fragment out of > 1 fragments is correctly
    # classified, then call the parent chopped
    else:
        parent['outcome'] = 'chopped'
    # We can't link the parent to all fragments. Link to the largest one
    _max_idx = _argmax(fragments['area'])
    parent['matched_to'] = fragments[_max_idx]['id']


# --- Numba functions where numpy does not suffice ---
# TODO write tests


@numba.njit
def _in1d(arr1, arr2):
    """
    Copy np.in1d logic for numba
    Five times faster than numpy #ohyeah
    """
    res = np.zeros(len(arr1), dtype=np.bool_)
    for i1 in range(len(arr1)):
        for v2 in arr2:
            if arr1[i1] == v2:
                res[i1] = 1
                break
    return res


@numba.jit(nopython=True)
def _in(val, arr):
    """
    Check if val is in array
    1.5x faster than val in np.array
    """
    for a in arr:
        if val == a:
            return True
    return False


@numba.jit(nopython=True)
def _argmax(arr):
    """
    Get index of max argument (np.argmax)
    Slightly faster than np.argmax
    """
    m = INT_NAN
    i = INT_NAN
    leng = len(arr)
    for j in range(leng):
        if arr[j] > m:
            m = arr[j]
            i = j
    return i
