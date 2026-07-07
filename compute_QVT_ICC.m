%% compute_QVT_ICC.m
% Computes per-feature test-retest reliability (ICC(2,1), two-way random,
% absolute agreement, single measurement) between two paired QVT feature
% matrices, then summarizes reliability using Koo & Li (2016) thresholds.
%
% INPUTS (variables must already exist in the workspace):
%   qvt_before : [n_cases x n_features] matrix (e.g., native voxel spacing)
%   qvt_after  : [n_cases x n_features] matrix (e.g., resampled/retest)
%
% OUTPUT:
%   icc_table  : table with one row per feature and its ICC value/category
%   summary    : counts and proportions per reliability category

assert(isequal(size(qvt_before), size(qvt_after)), ...
    'qvt_before and qvt_after must be the same size (n_cases x n_features).');

n_features = size(qvt_before, 2);
icc_values = nan(n_features, 1);

for f = 1:n_features
    icc_values(f) = icc_2_1([qvt_before(:, f), qvt_after(:, f)]);
end

% --- Classify each feature using Koo & Li (2016) reliability criteria ---
category = strings(n_features, 1);
category(icc_values >= 0.90)                       = "Excellent";
category(icc_values >= 0.75 & icc_values < 0.90)    = "Good";
category(icc_values >= 0.50 & icc_values < 0.75)    = "Moderate";
category(icc_values < 0.50)                         = "Poor";

feature_id = (1:n_features)';
icc_table = table(feature_id, icc_values, category, ...
    'VariableNames', {'Feature', 'ICC', 'Reliability'});
disp(icc_table);

% --- Summarize proportions ---
cats = ["Excellent", "Good", "Moderate", "Poor"];
counts = arrayfun(@(c) sum(category == c), cats)';
proportion = counts / n_features;
summary = table(cats', counts, proportion, ...
    'VariableNames', {'Category', 'N_Features', 'Proportion'});
disp(summary);

moderate_or_better = sum(icc_values >= 0.50);
fprintf('\n%d of %d evaluable features (%.1f%%) showed moderate-or-better reproducibility.\n', ...
    moderate_or_better, n_features, 100 * moderate_or_better / n_features);

writetable(icc_table, 'QVT_ICC_per_feature.csv');
writetable(summary, 'QVT_ICC_summary.csv');

%% ---- Local function: ICC(2,1), two-way random, absolute agreement ----
function icc = icc_2_1(X)
    % X: [n_subjects x 2] matrix (two repeated measurements per subject)
    [n, k] = size(X);
    grand_mean = mean(X(:));

    row_means = mean(X, 2);
    col_means = mean(X, 1);

    SSR = k * sum((row_means - grand_mean).^2);        % subjects
    SSC = n * sum((col_means - grand_mean).^2);         % raters/sessions
    SST = sum((X(:) - grand_mean).^2);                  % total
    SSE = SST - SSR - SSC;                              % residual/error

    MSR = SSR / (n - 1);
    MSC = SSC / (k - 1);
    MSE = SSE / ((n - 1) * (k - 1));

    icc = (MSR - MSE) / (MSR + (k - 1) * MSE + k * (MSC - MSE) / n);
end