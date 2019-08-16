def percentChange(startPoint, currentPoint):
    try:
        x = ((float(currentPoint) - startPoint) / abs(startPoint)) * 100.00
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.0001


def getPatterns(data, col, patternlength, customlabel=0, outcome_shift=3):
    n = len(data)
    patterns = []
    if not customlabel:

        for i in range(n - 1, patternlength + outcome_shift, -1):
            pat = data.iloc[i - patternlength - outcome_shift:i][col]
            pat = pat[:patternlength].append(pat[-1:])
            pat = pat.map(lambda x: percentChange(pat[0], x))

            patterns.append(pat)
            print(i) if i % 500 == 0 else None
    if customlabel:
        return
    return patterns


def getPatternsDailyZipline(data, col, patternlength, customlabel=0, outcome_shift=3):
    n = len(data)
    patterns = []
    if not customlabel:

        for i in range(n - 1, patternlength + outcome_shift, -1):
            pat = data.iloc[i - patternlength - outcome_shift:i][col]
            pat_without_label = pat[:patternlength]
            pat_last_day_price = pat[-1]
            label = 0
            if pat_last_day_price > pat_without_label[-1]:
                label = 1
            if pat_last_day_price < pat_without_label[-1]:
                label = -1

            pat_without_label = pat_without_label.map(lambda x: percentChange(pat_without_label[0], x))
            pattern = {'pat_without_label': pat_without_label, 'label': label}
            patterns.append(pattern)
            print(i) if i % 500 == 0 else None
    if customlabel:
        return
    return patterns


def rec(pastPattern, currentPattern):
    return sum(100.00 - abs(percentChange(p, c)) for p, c in zip(pastPattern[:], currentPattern)) / len(
        currentPattern)


def patternRecognition(pastPatterns, currentPattern, similarity):
    plot_pats = []
    for eachPattern in pastPatterns:
        sim = rec(eachPattern[:-1], currentPattern[:-1])
        if sim > similarity:
            similar_pattern = {'similarity': sim, 'pattern': eachPattern}
            plot_pats.append(similar_pattern)
    return plot_pats

def patternRecognitionDailyZipline(pastPatterns, currentPattern, similarity):
    plot_pats = []
    for eachPattern in pastPatterns:
        sim = rec(eachPattern['pat_without_label'], currentPattern['pat_without_label'])
        if sim > similarity:
            similar_pattern = eachPattern
            similar_pattern['similarity']=sim
            plot_pats.append(similar_pattern)
    return plot_pats


def getSimilarPaths(indice, patterns, similarity):
    current_pattern = patterns[indice]
    past_patterns = patterns[:indice]
    similar_paths = patternRecognition(pastPatterns=past_patterns,
                                       currentPattern=current_pattern,
                                       similarity=similarity)
    return current_pattern, similar_paths


def getSimilarPathsDailyZipline(indice, patterns, similarity):
    current_pattern = patterns[indice]
    past_patterns = patterns[indice + 1:]
    similar_paths = patternRecognitionDailyZipline(pastPatterns=past_patterns,
                                       currentPattern=current_pattern,
                                       similarity=similarity)
    return current_pattern, similar_paths


def getPlotArr(indices, patterns, similarity):
    if isinstance(indices, int):
        plot_arr = []
        while indices < 0:
            current_pattern, similar_paths = getSimilarPaths(indice=indices,
                                                             patterns=patterns,
                                                             similarity=similarity)
            print('pat Found for indice {}'.format(indices)) if len(similar_paths) > 0 else None
            if len(similar_paths) > 0:
                plot_arr.append((indices, current_pattern, similar_paths))
            indices += 1
            print(indices) if indices % 50 == 0 else None
        return plot_arr
    if isinstance(indices, list):
        plot_arr = []
        for ind in indices:
            current_pattern, similar_paths = getSimilarPaths(indice=ind,
                                                             patterns=patterns,
                                                             similarity=similarity)
            print('pat Found for indice {}'.format(ind)) if len(similar_paths) > 0 else None

            if len(similar_paths) > 0:
                plot_arr.append((ind, current_pattern, similar_paths))
            print(ind) if ind % 50 == 0 else None

        return plot_arr
