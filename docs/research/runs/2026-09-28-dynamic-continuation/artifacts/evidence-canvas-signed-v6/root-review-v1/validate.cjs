const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const ts = require("/Applications/Cursor.app/Contents/Resources/app/extensions/node_modules/typescript/lib/typescript.js");

const artifactDir = __dirname;
const originalPath = path.join(
  artifactDir,
  "dynamic-continuation-evidence.original.canvas.tsx",
);
const candidatePath = path.join(
  artifactDir,
  "dynamic-continuation-evidence.candidate.canvas.tsx",
);
const managedPath =
  "/Users/michael/.cursor/projects/Users-michael-Desktop-NTU-fyp-parabolab/canvases/dynamic-continuation-evidence.canvas.tsx";
const originalText = fs.readFileSync(originalPath, "utf8");
const candidateText = fs.readFileSync(candidatePath, "utf8");
const managedText = fs.readFileSync(managedPath, "utf8");
const sourceLocks = {
  "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/04z-all-positive-diffusivity-sharp-queries.md":
    "57ef1d86ddba30ce9d54f316b0eb2dc97f407f7aeb4446a66b3103c28e0aedd4",
  "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T90-root-correspondence.json":
    "2cec8c64716616c05383990fa4cbb143f21e42b58dde6b3a8121277ad56f85e7",
  "/Users/michael/Desktop/NTU/fyp/parabolab/formal/EstimatorIntegrity/UniformSliceConditioning.lean":
    "d50bd7145685480ab802270d4a5eae623205b373b70c1158b30cdbef50fd80fe",
  "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/06n-uniform-slice-conditioning-lean.md":
    "af6c63d6a6ed82180d68155d4b7047277dd440a2d23d651501abde46b98cc377",
  "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T86-root-correspondence.json":
    "b39b9cfb5b22e1185c95e191b3f7a85339b2f6314da4b5eb34ef66c332fdce0d",
};

function sha256(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}

function parse(filePath, text) {
  return ts.createSourceFile(
    filePath,
    text,
    ts.ScriptTarget.Latest,
    true,
    ts.ScriptKind.TSX,
  );
}

function topLevelConstants(sourceFile, text) {
  const result = new Map();
  for (const statement of sourceFile.statements) {
    if (!ts.isVariableStatement(statement)) continue;
    if ((statement.declarationList.flags & ts.NodeFlags.Const) === 0) continue;
    for (const declaration of statement.declarationList.declarations) {
      if (!ts.isIdentifier(declaration.name)) continue;
      result.set(
        declaration.name.text,
        text.slice(statement.getStart(sourceFile), statement.end),
      );
    }
  }
  return result;
}

function linkBindings(text) {
  return [...text.matchAll(/<Link\s+href=\{([A-Za-z_$][\w$]*)\}/g)].map(
    (match) => match[1],
  );
}

function counts(values) {
  const result = new Map();
  for (const value of values) result.set(value, (result.get(value) || 0) + 1);
  return result;
}

function localPathConstants(sourceFile) {
  const result = new Map();
  for (const statement of sourceFile.statements) {
    if (!ts.isVariableStatement(statement)) continue;
    for (const declaration of statement.declarationList.declarations) {
      if (
        ts.isIdentifier(declaration.name) &&
        declaration.initializer &&
        ts.isStringLiteral(declaration.initializer) &&
        declaration.initializer.text.startsWith("/")
      ) {
        result.set(declaration.name.text, declaration.initializer.text);
      }
    }
  }
  return result;
}

function jsxNodes(sourceFile, tagName) {
  const result = [];
  function visit(node) {
    if (
      ts.isJsxSelfClosingElement(node) &&
      node.tagName.getText(sourceFile) === tagName
    ) {
      result.push(node.getText(sourceFile));
    }
    ts.forEachChild(node, visit);
  }
  visit(sourceFile);
  return result;
}

function jsonArrayConstant(sourceFile, name) {
  for (const statement of sourceFile.statements) {
    if (!ts.isVariableStatement(statement)) continue;
    for (const declaration of statement.declarationList.declarations) {
      if (
        ts.isIdentifier(declaration.name) &&
        declaration.name.text === name &&
        declaration.initializer
      ) {
        return JSON.parse(declaration.initializer.getText(sourceFile));
      }
    }
  }
  throw new Error(`missing ${name}`);
}

function isLineSubsequence(earlier, later) {
  const originalLines = earlier.split("\n");
  const candidateLines = later.split("\n");
  let cursor = 0;
  for (const line of candidateLines) {
    if (cursor < originalLines.length && line === originalLines[cursor]) cursor += 1;
  }
  return cursor === originalLines.length;
}

function numericLiterals(sourceFile) {
  const result = [];
  function visit(node) {
    if (ts.isNumericLiteral(node)) result.push(node.getText(sourceFile));
    ts.forEachChild(node, visit);
  }
  visit(sourceFile);
  return result;
}

const originalSource = parse(originalPath, originalText);
const candidateSource = parse(candidatePath, candidateText);
const originalConstants = topLevelConstants(originalSource, originalText);
const candidateConstants = topLevelConstants(candidateSource, candidateText);
const changedConstants = [...originalConstants].filter(
  ([name, text]) => candidateConstants.get(name) !== text,
);
const originalLinks = linkBindings(originalText);
const candidateLinks = linkBindings(candidateText);
const originalLinkCounts = counts(originalLinks);
const candidateLinkCounts = counts(candidateLinks);
const missingLinkOccurrences = [...originalLinkCounts].filter(
  ([name, count]) => (candidateLinkCounts.get(name) || 0) < count,
);
const originalPaths = localPathConstants(originalSource);
const candidatePaths = localPathConstants(candidateSource);
const missingPaths = [...originalPaths].filter(
  ([name, value]) => candidatePaths.get(name) !== value,
);
const unresolvedPaths = [...candidatePaths].filter(([, value]) => !fs.existsSync(value));
const originalCharts = jsxNodes(originalSource, "LineChart");
const candidateCharts = jsxNodes(candidateSource, "LineChart");
const chartParity =
  originalCharts.length === candidateCharts.length &&
  originalCharts.every((chart, index) => chart === candidateCharts[index]);
const originalNumericCounts = counts(numericLiterals(originalSource));
const candidateNumericCounts = counts(numericLiterals(candidateSource));
const missingNumericLiterals = [...originalNumericCounts].filter(
  ([literal, count]) => (candidateNumericCounts.get(literal) || 0) < count,
);
const e4Pooled = jsonArrayConstant(candidateSource, "e4PooledCells");
const e4PerSeed = jsonArrayConstant(candidateSource, "e4PerSeedCells");
const e4Baselines = jsonArrayConstant(candidateSource, "e4ZeroQueryBaselines");
const imports = candidateSource.statements
  .filter(ts.isImportDeclaration)
  .map((statement) => statement.moduleSpecifier.text);
const requiredNarrative = [
  "D40–D42 · 全部固定正扩散的精确查询阶",
  "Θ(exp(γT)) 的最坏输入期望查询阶",
  "实际 Gaussian–Hilbert 采样器",
  "sup_v(E‖U_T−S_T^κv‖∞²)¹ᐟ²≤1/8",
  "D42 去掉了下方历史 D39 查询上界中的多项式因子",
  "付费工作仍只有 c exp(γT)≤W_point(T),W_profile(T)≤C exp(γT)(1+T)^A",
  "κ=0 的点值问题可一次查询解决，这不构成完整未知剖面的单查询结论",
  "本节冻结的 D40–D42 证明不使用后续 R20/R21 推广",
  "T86 · 实际均匀切片条件律与单步 KL",
  "主任务接受 · 28 个公开声明",
  "twoSlice_next_kl_toReal_le",
  "28 项按公开 definition、theorem 与 instance 合计，并非“28 个定理”",
  "不含完整 adaptive history、n 步链、seed simulation、padding、random stopping",
  "D37–D39 · 任意固定正扩散下的长期复杂度",
  "368,270,390",
];
const expectedT86Declarations = [
  "sliceFamily",
  "uniformSlice",
  "uniformSlice_isProbabilityMeasure",
  "uniformSlice_singleton",
  "compatibleEvent",
  "compatibleFamily",
  "mem_sliceFamily",
  "mem_compatibleFamily",
  "compatibleFamily_eq_filter_sdiff",
  "compatibleFamily_card",
  "conditionedSlice",
  "uniformSlice_compatibleEvent",
  "uniformSlice_compatibleEvent_pos",
  "conditionedSlice_eq_uniformCompatible",
  "conditionedSlice_isProbabilityMeasure",
  "unrevealedSet",
  "nextBit",
  "measurable_nextBit",
  "sliceParameter",
  "sliceRatio_le",
  "conditionedSlice_next_true",
  "conditionedSlice_next_true_zero",
  "conditionedSlice_next_true_one",
  "conditionedSlice_map_nextBit",
  "twoSlice_feasible",
  "twoSlice_ratio_bounds",
  "twoSlice_next_kl_ne_top",
  "twoSlice_next_kl_toReal_le",
];
const originalHash = sha256(originalText);
const candidateHash = sha256(candidateText);
const managedHash = sha256(managedText);
const originalLinesPreserved = isLineSubsequence(originalText, candidateText);
const checkedSourceLocks = Object.fromEntries(
  Object.entries(sourceLocks).map(([filePath, expected]) => {
    const actual = sha256(fs.readFileSync(filePath, "utf8"));
    return [filePath, { expected, actual, matches: actual === expected }];
  }),
);
const sourceLocksMatch = Object.values(checkedSourceLocks).every(
  ({ matches }) => matches,
);
const t86DeclarationsPresent = expectedT86Declarations.filter((name) =>
  candidateText.includes(name),
);

const result = {
  status:
    originalHash === "e2619ea14528c4e3d20e62ed2a3edb8cb2f3c175b47af4e31c9f1599f9e9fa41" &&
    managedHash === originalHash &&
    sourceLocksMatch &&
    originalLinesPreserved &&
    originalConstants.size === 82 &&
    changedConstants.length === 0 &&
    missingLinkOccurrences.length === 0 &&
    originalPaths.size === 63 &&
    missingPaths.length === 0 &&
    unresolvedPaths.length === 0 &&
    chartParity &&
    originalCharts.length === 5 &&
    missingNumericLiterals.length === 0 &&
    e4Pooled.length === 60 &&
    e4PerSeed.length === 180 &&
    e4Baselines.length === 36 &&
    imports.length === 1 &&
    imports[0] === "cursor/canvas" &&
    t86DeclarationsPresent.length === expectedT86Declarations.length &&
    requiredNarrative.every((value) => candidateText.includes(value))
      ? "PASS"
      : "FAIL",
  source_hashes: { original: originalHash, candidate: candidateHash, managed: managedHash },
  managed_canvas_unchanged_from_archived_original: managedHash === originalHash,
  checked_source_locks: checkedSourceLocks,
  original_lines_preserved_verbatim_in_order: originalLinesPreserved,
  original_top_level_constants: originalConstants.size,
  candidate_top_level_constants: candidateConstants.size,
  original_constants_preserved_verbatim: originalConstants.size - changedConstants.length,
  changed_original_constants: changedConstants.map(([name]) => name),
  original_link_occurrences: originalLinks.length,
  candidate_link_occurrences: candidateLinks.length,
  missing_original_link_occurrences: missingLinkOccurrences,
  original_local_path_constants: originalPaths.size,
  candidate_local_path_constants: candidatePaths.size,
  missing_or_changed_original_paths: missingPaths,
  unresolved_candidate_paths: unresolvedPaths,
  line_charts_original: originalCharts.length,
  line_charts_candidate: candidateCharts.length,
  line_charts_preserved_verbatim: chartParity,
  missing_original_numeric_literals: missingNumericLiterals,
  e4_records: {
    pooled: e4Pooled.length,
    per_seed: e4PerSeed.length,
    zero_query_baselines: e4Baselines.length,
    total_activity_text_preserved:
      originalText.includes("368,270,390") &&
      candidateText.includes("368,270,390"),
  },
  imports,
  embedded_data_only: !/\bfetch\s*\(|XMLHttpRequest|WebSocket/.test(candidateText),
  hardcoded_hex_colors: (candidateText.match(/#[0-9a-fA-F]{3,8}\b/g) || []).length,
  gradients: (candidateText.match(/(?:linear|radial)-gradient/g) || []).length,
  box_shadows: (candidateText.match(/boxShadow|box-shadow/g) || []).length,
  required_narrative_present: requiredNarrative.filter((value) =>
    candidateText.includes(value),
  ).length,
  required_narrative_total: requiredNarrative.length,
  t86_public_declarations_present: t86DeclarationsPresent.length,
  t86_public_declarations_expected: expectedT86Declarations.length,
};

console.log(JSON.stringify(result, null, 2));
process.exit(result.status === "PASS" ? 0 : 1);
