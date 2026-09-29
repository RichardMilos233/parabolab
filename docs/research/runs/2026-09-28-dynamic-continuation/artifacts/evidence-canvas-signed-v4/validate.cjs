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
const originalText = fs.readFileSync(originalPath, "utf8");
const candidateText = fs.readFileSync(candidatePath, "utf8");

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
const e4Pooled = jsonArrayConstant(candidateSource, "e4PooledCells");
const e4PerSeed = jsonArrayConstant(candidateSource, "e4PerSeedCells");
const e4Baselines = jsonArrayConstant(candidateSource, "e4ZeroQueryBaselines");
const imports = candidateSource.statements
  .filter(ts.isImportDeclaration)
  .map((statement) => statement.moduleSpecifier.text);
const requiredNarrative = [
  "D31 · 实际稳定图导数采样器已接受",
  "D32 · 已知基底高精度计算已接受",
  "c exp(γT) ≤ W(T) ≤ C exp(γT)(1+T)ᵃ",
  "γ=2d/(2s+d)",
  "不是去掉多项式因子的精确 Θ(exp(γT)) 总工作定理",
  "T75 的有限树矩 Lean 工作仍在进行，没有 PASS",
  "R14 是弱扩散/更一般谱隙范围的扩展候选",
  "fresh build 为 3511/3511",
  "四个失败尝试文件是事后整理的诊断摘要",
  "不是直接 tee 得到的字节归档",
];

const result = {
  status:
    originalConstants.size === 66 &&
    changedConstants.length === 0 &&
    missingLinkOccurrences.length === 0 &&
    originalPaths.size === 47 &&
    missingPaths.length === 0 &&
    unresolvedPaths.length === 0 &&
    chartParity &&
    e4Pooled.length === 60 &&
    e4PerSeed.length === 180 &&
    e4Baselines.length === 36 &&
    imports.length === 1 &&
    imports[0] === "cursor/canvas" &&
    requiredNarrative.every((value) => candidateText.includes(value))
      ? "PASS"
      : "FAIL",
  original_top_level_constants: originalConstants.size,
  candidate_top_level_constants: candidateConstants.size,
  original_constants_preserved_verbatim: originalConstants.size - changedConstants.length,
  historical_pre_t71_top_level_data_constants_preserved: 49,
  changed_original_constants: changedConstants.map(([name]) => name),
  original_link_occurrences: originalLinks.length,
  candidate_link_occurrences: candidateLinks.length,
  original_unique_link_bindings: originalLinkCounts.size,
  candidate_unique_link_bindings: candidateLinkCounts.size,
  missing_original_link_occurrences: missingLinkOccurrences,
  historical_pre_t71_link_bindings_preserved: 33,
  original_local_path_constants: originalPaths.size,
  candidate_local_path_constants: candidatePaths.size,
  missing_or_changed_original_paths: missingPaths,
  candidate_local_paths_resolved: candidatePaths.size - unresolvedPaths.length,
  unresolved_candidate_paths: unresolvedPaths,
  line_charts_original: originalCharts.length,
  line_charts_candidate: candidateCharts.length,
  line_charts_preserved_verbatim: chartParity,
  e4_records: {
    pooled: e4Pooled.length,
    per_seed: e4PerSeed.length,
    zero_query_baselines: e4Baselines.length,
    total_activity_text_preserved:
      originalText.includes("368,270,390") &&
      candidateText.includes("368,270,390"),
    replay_point_calls_text_preserved:
      originalText.includes("30,075,636") &&
      candidateText.includes("30,075,636"),
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
};

console.log(JSON.stringify(result, null, 2));
process.exit(result.status === "PASS" ? 0 : 1);
