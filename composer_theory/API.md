# `composer_theory` API Reference

本文档给出 `composer_theory` 当前公开模块中的类级 API 参考。

范围约定如下：

- 覆盖所有位于公开模块中的非下划线类。
- 同时记录这些类的公开属性、公开方法，以及实际构成对外接口的关键运算符协议。
- 不覆盖测试目录与内部下划线模块。

---

## 导入总览

- 基础领域对象：`composer_theory.domain`
- 枚举：`composer_theory.domain.enums.core`、`composer_theory.domain.enums.harmony`、`composer_theory.domain.enums.runtime`、`composer_theory.domain.enums.texture`
- 标识与引用对象：`composer_theory.domain.ids`
- 关系命中对象：`composer_theory.relations`
- 解析器：`composer_theory.resolve.resolver`
- 实现层对象：`composer_theory.implement`

---

## `composer_theory.domain.enums.core`

### `Degrees`

- 导入：`from composer_theory.domain.enums.core import Degrees`
- 说明：七个自然级位枚举，取值为 `I` 到 `VII`。
- 公开方法：无额外命名方法。
- 运算符协议：
  - `a + b -> Degrees`：做七级循环相加。
  - `a - b -> Degrees`：做七级循环相减。

### `NoteNames`

- 导入：`from composer_theory.domain.enums.core import NoteNames`
- 说明：自然音名枚举，成员为 `C`、`D`、`E`、`F`、`G`、`A`、`B`。
- 公开方法：无额外命名方法。
- 运算符协议：
  - `note_name + degree -> NoteNames`：按字母级数前进。
  - `note_name - degree -> NoteNames`：按字母级数后退。
  - `a | b -> Degrees`：返回两个音名之间的级位差。

### `Intervals`

- 导入：`from composer_theory.domain.enums.core import Intervals`
- 说明：音程序枚举，成员覆盖 `d1` 到 `M7` 的离散表示。
- 公开属性：
  - `degree`：该音程对应的 `Degrees`。
  - `semitones`：该音程对应的半音数。
- 运算符协议：
  - `a + b -> Intervals`：在级位与半音两个维度上合成音程。
  - `a - b -> Intervals`：在级位与半音两个维度上做差。

---

## `composer_theory.domain.enums.harmony`

### `Qualities`

- 导入：`from composer_theory.domain.enums.harmony import Qualities`
- 说明：和弦质量枚举，成员覆盖 `maj`、`min`、`sus2`、`sus4`、`maj7`、`min7`、`dim`、`aug`、`9/11/13` 等预定义质量。
- 公开方法：无新增公开方法。

### `Modes`

- 导入：`from composer_theory.domain.enums.harmony import Modes`
- 说明：七种基础调式枚举，成员为 `Ionian`、`Dorian`、`Phrygian`、`Lydian`、`Mixolydian`、`Aeolian`、`Locrian`。
- 公开方法：无新增公开方法。

### `VariantForm`

- 导入：`from composer_theory.domain.enums.harmony import VariantForm`
- 说明：调式形态枚举，成员为 `Base`、`Ascending`、`Descending`、`SubV`。
- 公开方法：无新增公开方法。

### `Tonality`

- 导入：`from composer_theory.domain.enums.harmony import Tonality`
- 说明：调式的大小属性枚举，成员为 `maj`、`min`。
- 公开方法：无新增公开方法。

### `ChromaticType`

- 导入：`from composer_theory.domain.enums.harmony import ChromaticType`
- 说明：半音化来源枚举，成员为 `Base`、`Degree`、`Mode`。
- 公开方法：无新增公开方法。

### `Functions`

- 导入：`from composer_theory.domain.enums.harmony import Functions`
- 说明：和声功能枚举，成员为 `Tonic`、`Dominant`、`Subdominant`、`Characteristic`。
- 公开方法：无新增公开方法。

### `ModeAccess`

- 导入：`from composer_theory.domain.enums.harmony import ModeAccess`
- 说明：调式进入方式枚举，成员为 `Relative`、`Substitute`。
- 公开方法：无新增公开方法。

---

## `composer_theory.domain.enums.runtime`

### `DynamicType`

- 导入：`from composer_theory.domain.enums.runtime import DynamicType`
- 说明：动态重音类型枚举，成员为 `Strong`、`Weak`。
- 公开方法：无新增公开方法。

### `DegreeVariant`

- 导入：`from composer_theory.domain.enums.runtime import DegreeVariant`
- 签名：`DegreeVariant(degree, variant=None)`
- 说明：运行时使用的“级位 + 形态”值对象。
- 公开属性：
  - `degree`：目标级位。
  - `variant`：可选的 `VariantForm`。
- 公开方法：无新增公开方法。
- 相关别名：`TargetPoint = DegreeVariant`。

### `TurningPoints`

- 导入：`from composer_theory.domain.enums.runtime import TurningPoints`
- 说明：和弦在旋律小调上行 / 下行形态中触发的转折点枚举。
- 公开方法：
  - `next() -> DegreeVariant`：返回当前转折点后续应该落到的目标级位 / 形态。

### `States`

- 导入：`from composer_theory.domain.enums.runtime import States`
- 说明：协和 / 不协和状态枚举，成员为 `Consonant`、`Dissonant`。
- 公开方法：无新增公开方法。

### `Voices`

- 导入：`from composer_theory.domain.enums.runtime import Voices`
- 说明：四部声部枚举，成员为 `Bass`、`Tenor`、`Alto`、`Soprano`。
- 公开方法：无新增公开方法。

### `LeadingType`

- 导入：`from composer_theory.domain.enums.runtime import LeadingType`
- 说明：连接方式枚举，成员为 `Step`、`Jump`、`Suspend`、`Transit`。
- 公开方法：无新增公开方法。

---

## `composer_theory.domain.enums.texture`

### `Textures`

- 导入：`from composer_theory.domain.enums.texture import Textures`
- 说明：织体类型枚举，成员为 `Columnar`、`Ascending`、`Triangular`、`Decomposition`。
- 公开方法：无新增公开方法。

---

## `composer_theory.domain.ids`

### `KeyId`

- 导入：`from composer_theory.domain.ids import KeyId`
- 签名：`KeyId(tonic, main_mode_type)`
- 说明：调性的稳定标识对象。
- 公开属性：
  - `tonic`：主音音名。
  - `main_mode_type`：主调式类型。
- 公开方法：无新增公开方法。

### `ModeId`

- 导入：`from composer_theory.domain.ids import ModeId`
- 签名：`ModeId(role, access=ModeAccess.Relative)`
- 说明：调式在调性中的身份对象。
- 公开属性：
  - `role`：可以是 `Modes`，也可以是相对级位 `Degrees`。
  - `access`：进入方式，默认为 `ModeAccess.Relative`。
- 公开方法：无新增公开方法。

### `RootVariantScaleRef`

- 导入：`from composer_theory.domain.ids import RootVariantScaleRef`
- 签名：`RootVariantScaleRef(root_degree, variant=VariantForm.Base)`
- 说明：按“根级位 + 形态”引用调式中的某个音阶。
- 公开属性：
  - `root_degree`：音阶根所在的级位。
  - `variant`：音阶形态。
- 公开方法：无新增公开方法。

### `SubVScaleRef`

- 导入：`from composer_theory.domain.ids import SubVScaleRef`
- 签名：`SubVScaleRef(target_degree)`
- 说明：按目标级位引用调式中的 SubV 音阶。
- 公开属性：
  - `target_degree`：SubV 所指向的目标级位。
- 公开方法：无新增公开方法。

### `ChordId`

- 导入：`from composer_theory.domain.ids import ChordId`
- 签名：`ChordId(scale_ref, composition)`
- 说明：和弦在调式中的身份对象。
- 公开属性：
  - `scale_ref`：`RootVariantScaleRef | SubVScaleRef`。
  - `composition`：相对根音的级位组成。
- 公开方法：
  - `is_subv -> bool`：判断该和弦是否来自 SubV 音阶引用。

---

## `composer_theory.domain.base_note`

### `BaseNote`

- 导入：`from composer_theory.domain.base_note import BaseNote`
- 签名：`BaseNote(note_name, shifts=0)`
- 说明：带拼写信息的基音对象，保留同音异名差异。
- 公开属性：
  - `note_name`：自然音名。
  - `shifts`：升降号数量，正数为升号，负数为降号。
  - `offset`：折算到 0 到 11 的音高类。
- 公开方法：
  - `respell(other) -> bool`：判断两个基音是否同音异名等价。
  - `from_name_and_offset(note_name, offset) -> BaseNote`：在给定音名下按音高类反推可拼写的基音。
- 运算符协议：
  - `note + interval -> BaseNote`：做音程上行。
  - `note - interval -> BaseNote`：做音程下行。
  - `a | b -> Intervals`：求两个基音之间的音程。

---

## `composer_theory.domain.scale`

### `Scale`

- 导入：`from composer_theory.domain.scale import Scale`
- 签名：`Scale(tonic, intervals)`
- 说明：由主音和 7 个音程序列构成的音阶对象。
- 公开属性：
  - `tonic`：音阶主音。
  - `intervals`：长度为 7 的 `Intervals` 元组。
  - `note_list`：音阶展开后的七个 `BaseNote`。
- 公开方法：
  - `pitch_class_set() -> frozenset[int]`：返回音阶包含的音高类集合。
  - `respell(other) -> bool`：判断两个音阶是否同音异名等价。
- 运算符协议：
  - `scale[degree] -> BaseNote`：按 `Degrees` 取某一级音。
  - `base_note in scale`：判断某个基音是否是音阶成员。
  - `scale | base_note -> Degrees | None`：反查基音所在级位。
  - `scale1 - scale2 -> ColorShift`：计算从 `scale2` 到 `scale1` 的色彩迁移。
  - `scale + color_shift -> Scale`：应用色彩迁移得到新音阶。
  - `iter(scale)`：按级位顺序遍历音阶基音。
  - `len(scale)`：返回 7。

---

## `composer_theory.domain.color_shift`

### `ColorShift`

- 导入：`from composer_theory.domain.color_shift import ColorShift`
- 签名：`ColorShift(src, diff, dst)`
- 说明：描述一个音阶从 `src` 音程序列经由 `diff` 主音移动后变为 `dst` 音程序列。
- 公开属性：
  - `src`：起点音程序列。
  - `diff`：主音位移音程。
  - `dst`：终点音程序列。
- 公开方法：无新增公开方法。

---

## `composer_theory.domain.dissonance`

### `Resolution`

- 导入：`from composer_theory.domain.dissonance import Resolution`
- 说明：不协和音的解决方向枚举，成员为 `NONE`、`STEP_UP`、`STEP_DOWN`、`STEP_EITHER`。
- 公开方法：无新增公开方法。

### `DissonanceRelation`

- 导入：`from composer_theory.domain.dissonance import DissonanceRelation`
- 签名：`DissonanceRelation(notes, kind, priority, min_moves, resolution)`
- 说明：一个不协和关系条目，记录参与音程、类别、优先级和解决方向。
- 公开属性：
  - `notes`：形成该关系的音程序集合。
  - `kind`：关系标签。
  - `priority`：用于张力评分的优先级。
  - `min_moves`：形成解决所需最少移动音数。
  - `resolution`：每个参与音程对应的解决方向。
- 公开方法：
  - `resolution_map() -> dict[Intervals, Resolution]`：把 `resolution` 元组转换为字典。

### `EdgeRule`

- 导入：`from composer_theory.domain.dissonance import EdgeRule`
- 签名：`EdgeRule(delta_semitones, kind, priority, earlier_resolution, later_resolution, min_moves=1)`
- 说明：二元音程不协和的规则对象。
- 公开属性：
  - `delta_semitones`
  - `kind`
  - `priority`
  - `earlier_resolution`
  - `later_resolution`
  - `min_moves`
- 公开方法：无新增公开方法。

### `SetRule`

- 导入：`from composer_theory.domain.dissonance import SetRule`
- 签名：`SetRule(kind, priority, min_moves, match, resolution_for_member)`
- 说明：多音集合不协和的规则对象。
- 公开属性：
  - `kind`
  - `priority`
  - `min_moves`
  - `match`
  - `resolution_for_member`
- 公开方法：无新增公开方法。

---

## `composer_theory.domain.quality`

### `Quality`

- 导入：`from composer_theory.domain.quality import Quality`
- 签名：`Quality(base, tensions=frozenset(), omits=frozenset())`
- 说明：和弦质量对象，由基础质量、扩展张力和省略音共同定义。
- 公开属性：
  - `base`：基础 `Qualities`。
  - `tensions`：附加张力音程集合。
  - `omits`：被省略的基础音程集合。
  - `name`：格式化后的质量名。
  - `dissonance_relations`：按当前质量推导出的不协和关系列表。
  - `dissonance_dict`：不协和关系的字典化视图。
- 公开方法：
  - `from_intervals(intervals) -> Quality`：从音程序集合反推出最匹配的质量。
  - `try_from_intervals(intervals) -> Quality | None`：宽松版的反推接口，失败时返回 `None`。
  - `composition() -> frozenset[Degrees]`：返回该质量需要包含的级位集合。

---

## `composer_theory.domain.chord`

### `Chord`

- 导入：`from composer_theory.domain.chord import Chord`
- 签名：`Chord(scale, composition=None)`
- 说明：建立在某个音阶之上的和弦对象；默认组成是三和弦 `I, III, V`。
- 公开属性：
  - `scale`：和弦所属音阶。
  - `composition`：相对根音的级位组成。
  - `base_notes`：和弦实际包含的基音集合。
  - `quality`：由组成反推出的 `Quality`。
  - `tension_score`：把质量中的不协和关系折算到 `0.0` 到 `10.0` 的张力分数。
  - `target_note_tendencies`：目标音倾向分布，键为 `Degrees`，值越大表示吸引越强。
- 公开方法：
  - `with_composition(composition) -> Chord`：在同一音阶上生成一个新组成的和弦。
  - `respell(other) -> bool`：判断两个和弦是否同音异名等价。
- 运算符协议：
  - `chord[degree] -> BaseNote`：返回和弦所在音阶的该级基音。
  - `base_note in chord`：判断某个基音是否属于和弦。
  - `chord | base_note -> Degrees | None`：反查某个基音在和弦组成中的级位。
  - `chord | degree -> Degrees | None`：判断某个级位是否属于和弦组成。
  - `chord1 - chord2 -> tuple[Transition, ColorShift]`：描述从 `chord2` 到 `chord1` 的质量迁移与色彩迁移。
  - `chord + (transition, color_shift) -> Chord`：把迁移对应用到当前和弦。
  - `iter(chord)`：遍历和弦基音。
  - `len(chord)`：返回和弦基音数量。

---

## `composer_theory.domain.transition`

### `Transition`

- 导入：`from composer_theory.domain.transition import Transition`
- 签名：`Transition(src, difference, dst)`
- 说明：描述两个和弦质量之间的迁移关系。
- 公开属性：
  - `src`：起点质量。
  - `difference`：根音位移的半音差，始终归一化到 `0` 到 `11`。
  - `dst`：终点质量。
- 公开方法：无新增公开方法。

---

## `composer_theory.domain.mode_specs`

### `ModeSpec`

- 导入：`from composer_theory.domain.mode_specs import ModeSpec`
- 签名：`ModeSpec(mode, variants, subv_profile, characteristic_degree)`
- 说明：单个调式的规格对象，决定基础音程序列、变体和特征级。
- 公开属性：
  - `mode`
  - `variants`
  - `subv_profile`
  - `characteristic_degree`
  - `supports_subv`：是否定义了 SubV 规格。
- 公开方法：无额外命名方法。

---

## `composer_theory.domain.mode`

### `Mode`

- 导入：`from composer_theory.domain.mode import Mode`
- 签名：`Mode(tonic, mode_type)`
- 说明：以某个主音和调式类型构成的调式对象。
- 公开属性：
  - `tonic`
  - `mode_type`
  - `spec`
  - `supports_subv`：该调式是否支持 SubV 音阶。
  - `characteristic_degree`：该调式的特征级。
  - `tonality`：该调式的大小属性。
- 公开方法：
  - `chord(scale_ref, composition=None) -> Chord`：先按 `scale_ref` 选音阶，再按组成生成和弦。
  - `respell(other) -> bool`：判断两个调式是否同音异名等价。
- 运算符协议：
  - `mode[scale_ref] -> Scale`：按 `RootVariantScaleRef` 或 `SubVScaleRef` 取音阶。
  - `mode[chord_id] -> Chord`：按 `ChordId` 取和弦。
  - `base_note in mode`：判断某个基音是否出现在任一公开音阶中。
  - `scale in mode`：判断某个音阶是否是该调式的某个公开音阶。
  - `chord in mode`：判断某个和弦是否是该调式的某个公开和弦。
  - `mode | base_note -> set[tuple[Degrees, VariantForm]]`：反查基音在哪些根级位 / 形态中出现。
  - `mode | scale -> set[tuple[Degrees, VariantForm]]`：反查音阶的身份。
  - `mode | chord -> set[tuple[Degrees, VariantForm]]`：反查和弦所属音阶的身份。

---

## `composer_theory.domain.key`

### `Key`

- 导入：`from composer_theory.domain.key import Key`
- 签名：`Key(tonic, main_mode_type)`
- 说明：以主音和主调式类型定义的调性对象。
- 公开属性：
  - `tonic`
  - `main_mode_type`
- 公开方法：
  - `respell(other) -> bool`：判断两个调性是否同音异名等价。
- 运算符协议：
  - `key[mode_type: Modes] -> Mode`：按绝对调式类型取调式。
  - `key[degree: Degrees] -> Mode`：按相对级位取关系调式。
  - `key[(degree, access)] -> Mode`：按级位和进入方式取调式；当前只支持 `ModeAccess.Relative`。
  - `key[mode_id: ModeId] -> Mode`：按 `ModeId` 取调式。
  - `mode in key`：判断某个调式是否属于当前调性。
  - `scale in key`、`base_note in key`、`chord in key`：判断对象是否被该调性包含。
  - `key | mode -> Modes | Degrees | None`：反查调式在调性中的角色。
  - `key | scale/base_note/chord -> set[Modes | Degrees]`：返回所有命中的角色集合。

---

## `composer_theory.relations.hit`

### `ResolveHit`

- 导入：`from composer_theory.relations import ResolveHit`
- 说明：所有关系命中对象的抽象基类。
- 公开方法：无新增语义方法。
- 运算符协议：
  - `str(hit)`：返回适合调试的简要字符串。

---

## `composer_theory.relations.mode_in_key`

### `ModeInKeyHit`

- 导入：`from composer_theory.relations import ModeInKeyHit`
- 签名：`ModeInKeyHit(key, mode_id, mode=None)`
- 说明：描述一个调式在某个调性中的命中结果；既能表示成员命中，也能表示“直接分析”命中。
- 公开属性：
  - `key`
  - `mode_id`
  - `mode`
  - `is_member`：是否存在明确的 `ModeId`。
  - `access`：调式进入方式；直接分析时为 `None`。
  - `role`：调式角色；直接分析时为 `None`。
  - `function_scores`：该调式骨架和弦在主调式基准下的功能分数。
  - `chromatic_score`：相对于主调式基准音阶的半音化分数。
  - `color`：`(Transition, ColorShift)`，表示骨架和弦相对于主和弦的色彩差。
- 公开方法：无额外命名方法。

---

## `composer_theory.relations.chord_in_mode`

### `ChordInModeHit`

- 导入：`from composer_theory.relations import ChordInModeHit`
- 签名：`ChordInModeHit(mode, chord_id, chord=None)`
- 说明：描述一个和弦在某个调式中的命中结果；既能表示成员命中，也能表示非成员直接分析。
- 公开属性：
  - `mode`
  - `chord_id`
  - `chord`
  - `is_member`：是否存在明确的 `ChordId`。
  - `function_scores`：和弦相对于调式主音的功能分数。
  - `chromatic_score`：和弦相对于调式基准音阶的半音化分数。
  - `color`：`(Transition, ColorShift)`，表示该和弦相对于调式主和弦的色彩差。
  - `composition`：成员命中时返回和弦组成；非成员命中会抛出 `AttributeError`。
  - `is_subv`：当前命中是否来自 SubV 音阶。
- 公开方法：
  - `turning_points() -> set[TurningPoints]`：返回当前和弦在上行 / 下行变体中的转折点集合。

---

## `composer_theory.relations.chord_in_key`

### `ChordInKeyHit`

- 导入：`from composer_theory.relations import ChordInKeyHit`
- 签名：`ChordInKeyHit(mode_in_key_hit, chord_id, chord=None)`
- 说明：描述一个和弦在某个调性中的命中结果；它是 `ModeInKeyHit` 与 `ChordId` 的复合分析结果。
- 公开属性：
  - `mode_in_key_hit`
  - `chord_id`
  - `chord`
  - `is_member`：是否存在明确的 `ChordId`。
  - `function_scores`：和弦相对于主调式基准的功能分数。
  - `chromatic_score`：和弦相对于主调式基准的半音化分数。
  - `color`：`(Transition, ColorShift)`，表示该和弦相对于主和弦的色彩差。
  - `composition`：成员命中时返回和弦组成；直接分析命中会抛出 `AttributeError`。
  - `is_subv`：当前命中是否来自 SubV 音阶。
- 公开方法：无额外命名方法。

---

## `composer_theory.resolve.resolver`

### `Resolver`

- 导入：`from composer_theory.resolve.resolver import Resolver`
- 签名：`Resolver()`
- 说明：统一的关系解析入口。
- 公开方法：
  - `resolve(a, b) -> list[ChordInModeHit | ModeInKeyHit | ChordInKeyHit]`：支持以下输入对，顺序可交换：
    - `Chord` 与 `Mode`
    - `Mode` 与 `Key`
    - `Chord` 与 `Key`

---

## `composer_theory.implement.note`

### `Note`

- 导入：`from composer_theory.implement import Note`
- 签名：`Note(base_note, octave)`
- 说明：带八度信息的实际音高对象。
- 公开属性：
  - `base_note`
  - `octave`
  - `height`：线性化后的绝对高度，计算方式为 `12 * octave + base_note.offset`。
- 公开方法：无新增公开方法。

---

## `composer_theory.implement.arrangement`

### `Arrangement`

- 导入：`from composer_theory.implement import Arrangement`
- 签名：`Arrangement()`
- 说明：四部声部分配容器。
- 公开属性：
  - `note_dict`：`Voices -> Note | None` 的映射。
- 公开方法：无额外命名方法。
- 运算符协议：
  - `arrangement[voice] -> Note | None`：读取某个声部上的音。
  - `arrangement[voice] = note`：写入某个声部上的音。

---

## 备注

- `composer_theory.domain` 这个聚合模块直接再导出了 `Key`、`Mode`、`Scale`、`Chord`、`BaseNote`、`Transition` 以及各类 `Id / Ref` 类型，适合大多数使用场景。
- `composer_theory.relations` 聚合导出了四个命中对象：`ResolveHit`、`ModeInKeyHit`、`ChordInModeHit`、`ChordInKeyHit`。
- `composer_theory.implement` 聚合导出了 `Note` 与 `Arrangement`。
- 对于依赖 `[]`、`|`、`+`、`-` 的对象，推荐同时阅读主文档 `README.md` 中对应章节，因为那里对语义边界和理论背景解释得更完整。
