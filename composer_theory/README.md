# `composer_theory` 文档

本文档分为两篇。

第一篇讨论 `composer_theory.domain` 中的基础乐理对象。  
第二篇讨论 `composer_theory.relations` 与 `composer_theory.resolve` 中的关系命中对象与解析器。  

在本文档中，重点不放在“调用技巧”，而放在“形式化定义、对象之间的结构关系，以及公开接口的语义边界”。

---

## API 参考

完整的 API 参考文档见 [API.md](./API.md)。

该文档覆盖当前公开模块中的全部公开类、它们的公开属性、公开方法，以及本包核心的索引 / 运算符协议（如 `[]`、`in`、`|`、`+`、`-`）。

---

## PyPI API 总览

PyPI 页面只会直接渲染本 README，不会单独渲染 `API.md`。  
因此，这里补一份面向 PyPI 访问者的公开 API 总览；更完整的签名、属性说明和运算符协议仍见 [API.md](./API.md)。

### `composer_theory.domain`

- `BaseNote`: `respell`, `from_name_and_offset`
- `Scale`: `pitch_class_set`, `respell`
- `ColorShift`: 无额外命名公开方法
- `Resolution`: 无额外命名公开方法
- `DissonanceRelation`: `resolution_map`
- `EdgeRule`: 无额外命名公开方法
- `SetRule`: 无额外命名公开方法
- `KeyId`: 无额外命名公开方法
- `ModeId`: 无额外命名公开方法
- `RootVariantScaleRef`: 无额外命名公开方法
- `SubVScaleRef`: 无额外命名公开方法
- `ChordId`: `is_subv`
- `Transition`: 无额外命名公开方法
- `ModeSpec`: `supports_subv`
- `Quality`: `name`, `dissonance_relations`, `dissonance_dict`, `from_intervals`, `try_from_intervals`, `composition`
- `Chord`: `tension_score`, `target_note_tendencies`, `with_composition`, `respell`
- `Mode`: `supports_subv`, `chord`, `characteristic_degree`, `tonality`, `respell`
- `Key`: `respell`

### `composer_theory.domain.enums`

- `Degrees`: 无额外命名公开方法
- `NoteNames`: 无额外命名公开方法
- `Intervals`: `degree`, `semitones`
- `Qualities`: 无额外命名公开方法
- `Modes`: 无额外命名公开方法
- `VariantForm`: 无额外命名公开方法
- `Tonality`: 无额外命名公开方法
- `ChromaticType`: 无额外命名公开方法
- `Functions`: 无额外命名公开方法
- `ModeAccess`: 无额外命名公开方法
- `DynamicType`: 无额外命名公开方法
- `DegreeVariant`: 无额外命名公开方法
- `TurningPoints`: `next`
- `States`: 无额外命名公开方法
- `Voices`: 无额外命名公开方法
- `LeadingType`: 无额外命名公开方法
- `Textures`: 无额外命名公开方法

### `composer_theory.relations` / `composer_theory.resolve`

- `ResolveHit`: 无额外命名公开方法
- `ModeInKeyHit`: `is_member`, `access`, `role`, `function_scores`, `chromatic_score`, `color`
- `ChordInModeHit`: `is_member`, `function_scores`, `chromatic_score`, `color`, `turning_points`
- `ChordInKeyHit`: `is_member`, `function_scores`, `chromatic_score`, `color`
- `Resolver`: `resolve`

### `composer_theory.implement`

- `Note`: 无额外命名公开方法
- `Arrangement`: 无额外命名公开方法

---

## 目录

- [基础乐理篇](#part-foundation)
- [第一章 基音、音程、音阶](#chapter-1)
- [1.1 枚举与查找规则](#section-1-1)
- [1.2 基础集合](#section-1-2)
- [1.3 音级](#section-1-3)
- [1.4 音名](#section-1-4)
- [1.5 音程](#section-1-5)
- [1.6 基音](#section-1-6)
- [1.7 基音之间的关系](#section-1-7)
- [1.8 基音与音程的运算](#section-1-8)
- [1.9 音阶](#section-1-9)
- [1.10 七声音阶的合法性](#section-1-10)
- [1.11 音阶与基音的关系](#section-1-11)
- [1.12 色彩迁移](#section-1-12)
- [1.13 最小用例](#section-1-13)
- [第二章 和弦](#chapter-2)
- [2.1 和弦的基本定义](#section-2-1)
- [2.2 和弦的基音集合](#section-2-2)
- [2.3 和弦中的相对级位](#section-2-3)
- [2.4 和弦质量](#section-2-4)
- [2.5 和弦质量的反推](#section-2-5)
- [2.6 不协和关系](#section-2-6)
- [2.7 解决方向](#section-2-7)
- [2.8 张力分数](#section-2-8)
- [2.9 目标音倾向](#section-2-9)
- [2.10 功能迁移](#section-2-10)
- [2.11 和弦差](#section-2-11)
- [2.12 最小用例](#section-2-12)
- [第三章 调式](#chapter-3)
- [3.1 调式规格](#section-3-1)
- [3.2 七种基础调式](#section-3-2)
- [3.3 调式形态](#section-3-3)
- [3.4 调式](#section-3-4)
- [3.5 调式的基础音阶](#section-3-5)
- [3.6 调式的派生音阶](#section-3-6)
- [3.7 调式的和弦构造](#section-3-7)
- [3.8 特征级](#section-3-8)
- [3.9 调式的大小属性](#section-3-9)
- [3.10 调式索引与和弦编号](#section-3-10)
- [3.11 最小用例](#section-3-11)
- [第四章 调性](#chapter-4)
- [4.1 调性的基本定义](#section-4-1)
- [4.2 调性的主调式](#section-4-2)
- [4.3 调性中的同主音入口](#section-4-3)
- [4.4 调性中的关系调式入口](#section-4-4)
- [4.5 调性与 SubV 的边界](#section-4-5)
- [4.6 调性的模式空间](#section-4-6)
- [4.7 调性的反查](#section-4-7)
- [4.8 调性编号](#section-4-8)
- [4.9 调性索引与调式编号](#section-4-9)
- [4.10 最小用例](#section-4-10)
- [关系解析篇](#part-relations)
- [第五章 关系层的公开对象](#chapter-5)
- [5.1 导出集合](#section-5-1)
- [5.2 命中的一般形式](#section-5-2)
- [5.3 命中的共同特征](#section-5-3)
- [5.4 公开属性与内部属性的边界](#section-5-4)
- [5.5 最小用例](#section-5-5)
- [第六章 ChordInModeHit](#chapter-6)
- [6.1 所表示的关系](#section-6-1)
- [6.2 基本字段](#section-6-2)
- [6.3 成员命中与非成员命中](#section-6-3)
- [6.4 和弦身份](#section-6-4)
- [6.5 功能分数](#section-6-5)
- [6.6 半音化分数](#section-6-6)
- [6.7 色彩结果](#section-6-7)
- [6.8 转折点](#section-6-8)
- [6.9 字符串表示](#section-6-9)
- [6.10 最小用例](#section-6-10)
- [第七章 ModeInKeyHit](#chapter-7)
- [7.1 所表示的关系](#section-7-1)
- [7.2 基本字段](#section-7-2)
- [7.3 成员命中与直接分析命中](#section-7-3)
- [7.4 调式身份](#section-7-4)
- [7.5 功能分数](#section-7-5)
- [7.6 半音化分数](#section-7-6)
- [7.7 色彩结果](#section-7-7)
- [7.8 字符串表示](#section-7-8)
- [7.9 最小用例](#section-7-9)
- [第八章 ChordInKeyHit](#chapter-8)
- [8.1 所表示的关系](#section-8-1)
- [8.2 复合结构](#section-8-2)
- [8.3 公开字段](#section-8-3)
- [8.4 调式成员性](#section-8-4)
- [8.5 上下文读取方式](#section-8-5)
- [8.6 功能分数](#section-8-6)
- [8.7 半音化分数](#section-8-7)
- [8.8 色彩结果](#section-8-8)
- [8.9 成员命中与直接分析命中](#section-8-9)
- [8.10 字符串表示](#section-8-10)
- [8.11 最小用例](#section-8-11)
- [第九章 Resolver](#chapter-9)
- [9.1 统一解析入口](#section-9-1)
- [9.2 支持的输入对](#section-9-2)
- [9.3 Chord -> Mode 的解析](#section-9-3)
- [9.4 Mode -> Key 的解析](#section-9-4)
- [9.5 Chord -> Key 的解析](#section-9-5)
- [9.6 返回值的意义](#section-9-6)
- [9.7 最小用例](#section-9-7)

---

<a id="part-foundation"></a>
## 基础乐理篇

本篇对应下列代码文件：

- `domain/enums/__init__.py`
- `domain/enums/_lookup.py`
- `domain/enums/core.py`
- `domain/enums/harmony.py`
- `domain/enums/runtime.py`
- `domain/enums/texture.py`
- `domain/base_note.py`
- `domain/scale.py`
- `domain/color_shift.py`
- `domain/chord.py`
- `domain/dissonance.py`
- `domain/transition.py`
- `domain/quality.py`
- `domain/ids.py`
- `domain/mode_specs.py`
- `domain/mode.py`
- `domain/key.py`

这些文件共同构成一个由低到高的理论层级：

```text
枚举与基础集合
-> 基音
-> 音程
-> 音阶
-> 和弦与和弦质量
-> 调式
-> 调性
```

在这个体系中，每个对象都不是凭经验命名，而是由更基础的对象严格构造出来。

---

<a id="chapter-1"></a>
## 第一章 基音、音程、音阶

本章对应文件：

- `domain/enums/__init__.py`
- `domain/enums/_lookup.py`
- `domain/enums/core.py`
- `domain/enums/harmony.py`
- `domain/enums/runtime.py`
- `domain/enums/texture.py`
- `domain/base_note.py`
- `domain/scale.py`
- `domain/color_shift.py`

<a id="section-1-1"></a>
### 1.1 枚举与查找规则

在本包中，最基本的理论单位并不是直接写成字符串，而是先写成枚举。  
这样做的目的，是使每个理论名词同时具备：

1. 固定取值范围；
2. 可比较性；
3. 可索引性；
4. 可从值反查枚举成员的能力。

其中，`LookupEnum` 给出统一的查找规则。  
若某个值可以合法地对应到某个枚举成员，则返回该成员；  
若不能对应，则抛出错误。

因此，枚举在本包中不仅承担“命名”的作用，也承担“合法性约束”的作用。

<a id="section-1-2"></a>
### 1.2 基础集合

在本章中，先约定以下几个基础集合。

设：

- `N = {C, D, E, F, G, A, B}` 为自然音名集合；
- `D = {I, II, III, IV, V, VI, VII}` 为音级集合；
- `P = {0, 1, 2, ..., 11}` 为十二音高类集合。

此外，还要约定若干扩展集合。

第一，形态集合：

- `V = {Base, Ascending, Descending, SubV}`

第二，和声功能集合：

- `F = {Tonic, Dominant, Subdominant, Characteristic}`

第三，织体集合：

- `T = {Columnar, Ascending, Triangular, Decomposition}`

第四，运行时导向集合：

- 动态类型：`{Strong, Weak}`
- 状态：`{Consonant, Dissonant}`
- 声部：`{Bass, Tenor, Alto, Soprano}`
- 连接类型：`{Step, Jump, Suspend, Transit}`

由此可见，`domain/enums` 的任务，是为后续全部理论对象提供一套离散而稳定的语义坐标系。

<a id="section-1-3"></a>
### 1.3 音级

音级对应 `Degrees`。  
它是一个七项循环系统，而不是普通整数系统。

因此，对于任意 `a, b ∈ D`：

- `a + b` 表示在七级循环中向前推进；
- `a - b` 表示在七级循环中做相对回退。

这说明，在本包中，音级的本质是“相对位置”，不是“绝对数量”。

<a id="section-1-4"></a>
### 1.4 音名

音名对应 `NoteNames`。  
每个自然音名都对应一个基础音高类：

- `C -> 0`
- `D -> 2`
- `E -> 4`
- `F -> 5`
- `G -> 7`
- `A -> 9`
- `B -> 11`

此外，音名还和音级发生关系。

若 `n ∈ N`，`d ∈ D`，则：

- `n + d` 表示以 `n` 为出发点，沿音名字母循环前进 `d` 级后的结果；
- `n - d` 表示沿音名字母循环后退 `d` 级后的结果；
- `n1 | n2` 表示两个音名之间的级位差。

因此，音名在本包中不是单纯标签，而是携带字母顺序结构的对象。

<a id="section-1-5"></a>
### 1.5 音程

音程对应 `Intervals`。  
一个音程由两项确定：

```text
i = (d, p)
```

其中：

- `d ∈ D` 表示级位差；
- `p ∈ P` 表示半音差。

例如：

- `P1 = (I, 0)`
- `m2 = (II, 1)`
- `M2 = (II, 2)`
- `m3 = (III, 3)`
- `M3 = (III, 4)`
- `P5 = (V, 7)`

因此，音程不是先有名称再附带意义，而是先有“级位差 + 半音差”的二元结构，再由此确定名称。

<a id="section-1-6"></a>
### 1.6 基音

基音对应 `BaseNote`。  
在本包中，一个基音由下列两项构成：

```text
t = (n, s)
```

其中：

- `n ∈ N`；
- `s` 为升降记号数量，当前限制为 `-2 <= s <= 2`。

由此定义该基音的音高类为：

```text
pc(t) = (value(n) + s) mod 12
```

因此，基音同时包含：

1. 记谱上的拼写信息；
2. 实际上的音高类信息。

这就意味着：

- `C#` 与 `Db` 可以同音高类；
- 但在本包中，它们不是同一个基音。

<a id="section-1-7"></a>
### 1.7 基音之间的关系

设有两个基音：

```text
t1 = (n1, s1)
t2 = (n2, s2)
```

则从 `t1` 到 `t2` 的关系由两部分确定：

1. 音名之间的级位差；
2. 音高类之间的半音差。

因此，基音对基音的运算 `t1 | t2` 返回一个音程。  
这说明，在本包中，音程是通过两个基音的差被计算出来的，而不是凭经验直接赋名。

<a id="section-1-8"></a>
### 1.8 基音与音程的运算

若 `t` 为基音，`i` 为音程，则本包定义：

- `t + i`
- `t - i`

其意义分别是：

- 由一个已知基音，沿音程正向构造目标基音；
- 由一个已知基音，沿音程反向回推目标基音。

在这个过程中，系统既要保持音名字母的正确推进，也要保持目标音高类的正确落位。  
若某个结果需要超过当前允许的升降记号数量，则该构造不成立。

<a id="section-1-9"></a>
### 1.9 音阶

音阶对应 `Scale`。  
一个音阶由：

1. 一个主音；
2. 一个长度为 7 的音程序列；

共同确定。

因此，一个音阶可以写作：

```text
X = (t0; i1, i2, ..., i7)
```

其中：

- `t0` 为主音；
- `i1 = P1`；
- `i1, ..., i7` 依次给出七个级位相对主音的位置。

音阶中的第 `r` 级音定义为：

```text
X[r] = t0 + ir
```

其中 `r ∈ D`。

因此，音阶不是“七个音的集合”，而是“一个主音下的有序七项结构”。

<a id="section-1-10"></a>
### 1.10 七声音阶的合法性

在本包中，一个 `Scale` 合法，当且仅当：

1. 音程序列长度为 7；
2. 第一项为 `P1`；
3. 每一级都能在当前拼写限制下构造出合法基音。

由此可见，本包中的七声音阶既受乐理结构约束，也受拼写实现约束。

<a id="section-1-11"></a>
### 1.11 音阶与基音的关系

设 `X` 为音阶，`t` 为基音。  
则音阶可以对基音做反查。

若存在 `r ∈ D` 使得：

```text
X[r] = t
```

则称 `t` 属于该音阶，且其级位为 `r`。  
若不存在这样的 `r`，则称 `t` 不属于该音阶。

因此，本包中的“属于音阶”是严格拼写意义下的属于，而不是仅按音高类近似判断。

<a id="section-1-12"></a>
### 1.12 色彩迁移

色彩迁移对应 `ColorShift`。  
它不是和弦概念，而是音阶概念。

一个色彩迁移由三项确定：

```text
CS = (src, diff, dst)
```

其中：

- `src` 为起始音阶的七音程序列；
- `diff` 为主音之间的音程差；
- `dst` 为目标音阶的七音程序列。

因此，色彩迁移描述的是：

从一个音阶到另一个音阶时，
主音如何变化，
内部级位分布又如何变化。

它不是“调高若干半音”的单维变换，而是“主音 + 音阶结构”的联合变换。

<a id="section-1-13"></a>
### 1.13 最小用例

下面这个例子同时覆盖了：

1. `BaseNote + Intervals`
2. `BaseNote | BaseNote`
3. `Scale[Degrees]`

```python
from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.enums.core import Degrees, Intervals, NoteNames
from composer_theory.domain.scale import Scale

c = BaseNote(NoteNames.C)
g = c + Intervals.P5

c_major = Scale(
    tonic=c,
    intervals=(
        Intervals.P1,
        Intervals.M2,
        Intervals.M3,
        Intervals.P4,
        Intervals.P5,
        Intervals.M6,
        Intervals.M7,
    ),
)

assert g == c_major[Degrees.V]
assert (c | g) == Intervals.P5
```

---

<a id="chapter-2"></a>
## 第二章 和弦

本章对应文件：

- `domain/chord.py`
- `domain/dissonance.py`
- `domain/transition.py`
- `domain/quality.py`

<a id="section-2-1"></a>
### 2.1 和弦的基本定义

和弦对应 `Chord`。  
在本包中，一个和弦由：

1. 一个音阶；
2. 一个相对根音的音级集合；

共同确定。

因此，一个和弦可以写作：

```text
C = (X, A)
```

其中：

- `X` 为根音音阶；
- `A ⊆ D`；
- `I ∈ A`。

这里 `I ∈ A` 是强制条件。  
因为在本包中，`I` 表示和弦根音本身。  
若缺少 `I`，则这个结构不能构成合法和弦。

<a id="section-2-2"></a>
### 2.2 和弦的基音集合

设 `C = (X, A)` 为一个和弦。  
则它的实际基音集合定义为：

```text
Notes(C) = { X[r] | r ∈ A }
```

因此，和弦中的音不是单独逐个记录的，  
而是由一个“根音音阶 + 相对音级集合”共同推导出来的。

<a id="section-2-3"></a>
### 2.3 和弦中的相对级位

在本包中，和弦内部的级位始终相对和弦根音计算。  
例如：

- `I` 表示根音；
- `III` 表示和弦内部第三音；
- `V` 表示和弦内部第五音。

这说明，`Chord.composition` 的坐标系不是“相对调式主音”，而是“相对和弦根音”。

<a id="section-2-4"></a>
### 2.4 和弦质量

和弦质量对应 `Quality`。  
一个和弦质量由三部分构成：

```text
Q = (b, T, O)
```

其中：

- `b` 为基础质量；
- `T` 为张力集合；
- `O` 为省略集合。

基础质量来自 `Qualities`，例如：

- `maj`
- `min`
- `dim`
- `maj7`
- `min7`
- `dim7`
- `min7b5`

因此，和弦质量不是一个单独名字，而是由骨架、扩展和删减共同组成的结构。

<a id="section-2-5"></a>
### 2.5 和弦质量的反推

在本包中，`Quality` 通常不是手动指定，而是通过和弦内部音程集合反推得到。

其基本思想是：

1. 先由和弦组成音得到相对根音的音程集合；
2. 再在既有基础质量中寻找最匹配的一项；
3. 把额外音记为张力；
4. 把缺失音记为省略。

因此，质量判断不是任意命名，而是一个受限的最优匹配过程。

<a id="section-2-6"></a>
### 2.6 不协和关系

和弦内部的不协和关系由 `DissonanceRelation` 表示。  
一个不协和关系至少包含：

1. 参与该关系的音程集合；
2. 关系类别；
3. 优先级；
4. 最小解决移动数；
5. 各成员音的解决方向。

例如，当前系统会识别：

- 小二度
- 大二度
- 纯四度
- 三全音
- 小七度
- 大七度
- 增三和弦音集

因此，本包中的不协和不是抽象感受，而是可列举、可评分、可推导解决方向的结构。

<a id="section-2-7"></a>
### 2.7 解决方向

不协和关系中的解决方向由 `Resolution` 表示。  
当前允许：

- `NONE`
- `STEP_UP`
- `STEP_DOWN`
- `STEP_EITHER`

这说明，在本包中，和弦内部的张力不仅被识别，还被赋予了后续运动倾向。

<a id="section-2-8"></a>
### 2.8 张力分数

设 `C` 为一个和弦。  
则 `C.tension_score` 表示它内部不协和关系累积后的总体张力强度。

该分数由规则优先级汇总后得到，并被裁剪在 `0` 到 `10` 的范围内。  
因此，它不是任意评价，而是一个由规则系统生成的定量结果。

<a id="section-2-9"></a>
### 2.9 目标音倾向

`C.target_note_tendencies` 表示：

若和弦内部某些不协和音按规则解决，  
则它们更可能导向哪些相对级位。

因此，在本包中，一个和弦不仅是静态集合，  
也隐含了从自身结构推出的未来运动方向。

<a id="section-2-10"></a>
### 2.10 功能迁移

功能迁移对应 `Transition`。  
它由三项组成：

```text
TR = (Q1, k, Q2)
```

其中：

- `Q1` 为源和弦质量；
- `k` 为根音半音差；
- `Q2` 为目标和弦质量。

因此，功能迁移描述的是：

一个和弦从某种质量变到另一种质量时，  
在根音位置上发生了怎样的位移。

<a id="section-2-11"></a>
### 2.11 和弦差

设 `C1`、`C2` 为两个和弦。  
则在本包中，`C1 - C2` 的结果不是一个和弦，而是：

```text
(Transition, ColorShift)
```

这意味着：

和弦与和弦之间的差，被拆成了两部分：

1. 和弦质量与根音位置的变化；
2. 所属音阶结构的色彩变化。

因此，和弦变化在本包中总是被看作“功能层变化”与“色彩层变化”的联合。

<a id="section-2-12"></a>
### 2.12 最小用例

下面这个例子展示：

1. 如何从音阶构造和弦
2. 如何读取质量
3. 如何读取张力分数

```python
from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.chord import Chord
from composer_theory.domain.enums.core import Degrees, Intervals, NoteNames
from composer_theory.domain.scale import Scale

c_ionian = Scale(
    tonic=BaseNote(NoteNames.C),
    intervals=(
        Intervals.P1,
        Intervals.M2,
        Intervals.M3,
        Intervals.P4,
        Intervals.P5,
        Intervals.M6,
        Intervals.M7,
    ),
)

cmaj7 = Chord(c_ionian, frozenset({Degrees.I, Degrees.III, Degrees.V, Degrees.VII}))

assert str(cmaj7) == "Cmaj7"
assert cmaj7.quality.name == "maj7"
assert cmaj7.tension_score >= 0
```

---

<a id="chapter-3"></a>
## 第三章 调式

本章对应文件：

- `domain/ids.py`
- `domain/mode_specs.py`
- `domain/mode.py`

<a id="section-3-1"></a>
### 3.1 调式规格

调式规格对应 `ModeSpec`。  
一个调式规格由三部分组成：

```text
M = (name, variants, c)
```

其中：

- `name` 为调式名称；
- `variants` 为从形态到七音程序列的映射；
- `c ∈ D` 为特征级。

因此，调式规格并不是一个具体实例，  
而是一套“怎样构造该调式”的公共规则。

<a id="section-3-2"></a>
### 3.2 七种基础调式

当前系统的基础调式为：

- Ionian
- Dorian
- Phrygian
- Lydian
- Mixolydian
- Aeolian
- Locrian

这些调式的基础形态都在 `MODE_SPECS` 中预先写定。  
因此，调式实例化时不是重新发明音阶，而是调用既有规格。

<a id="section-3-3"></a>
### 3.3 调式形态

对于某些调式，除了基础形态 `Base` 外，还可能存在：

- `Ascending`
- `Descending`

这说明，在本包中，一个调式不是必然只对应一个音阶。  
它可以对应若干相关形态，而这些形态共享同一个调式身份。

<a id="section-3-4"></a>
### 3.4 调式

调式对应 `Mode`。  
一个调式由：

1. 一个主音；
2. 一个调式类型；

共同确定。

因此，一个调式可写作：

```text
mode = (t, m)
```

其中：

- `t` 为主音；
- `m` 为调式类型。

由此，调式会为其全部合法形态生成对应音阶。

<a id="section-3-5"></a>
### 3.5 调式的基础音阶

设 `mode = (t, m)`，`v` 为某个形态。  
则该调式在形态 `v` 下的音阶定义为：

```text
Scale_v(mode) = (t; profile_v(m))
```

因此，调式中的音阶是由“主音 + 规格中的音程序列”共同确定的。

<a id="section-3-6"></a>
### 3.6 调式的派生音阶

设 `r ∈ D`。  
则 `mode[RootVariantScaleRef(r, v)]` 表示：

在调式 `mode` 的 `v` 形态中，  
取第 `r` 级为新主音后形成的派生音阶。

这里的关键不在于“重新挑七个音”，  
而在于“保持原级位顺序，仅改变参考主音”。

<a id="section-3-7"></a>
### 3.7 调式的和弦构造

调式可以通过索引生成和弦。  
若给定：

- 根音级位 `r`
- 调式形态 `v`
- 和弦组成集合 `A`

则调式中的和弦可写作：

```text
Chord(mode[RootVariantScaleRef(r, v)], A)
```

因此，调式是和弦构造的上层背景。  
和弦不是脱离调式凭空生成，而是先通过调式中的某一级音阶建立起来。

<a id="section-3-8"></a>
### 3.8 特征级

每个调式都有一个特征级 `characteristic_degree`。  
它表示该调式相对于其它调式最有辨识度的级位。

因此，在本包中，调式的个性不是模糊描述，而是通过一个明确的特征级被记录下来。

<a id="section-3-9"></a>
### 3.9 调式的大小属性

调式还具有 `tonality`，即大小属性。  
当前实现通过基础形态中的第三音程来判断：

- 若第三度为大三度，则视为 `maj`；
- 若第三度为小三度，则视为 `min`。

因此，调式的大小属性在本包中是从结构中推导出来的，而不是额外手写标签。

<a id="section-3-10"></a>
### 3.10 调式索引与和弦编号

为了使“调式索引和弦”成为一个稳定而可复用的操作，  
本包定义了 `ChordId`。

一个 `ChordId` 由三部分组成：

```text
CID = (scale_ref, A)
```

其中：

- `scale_ref ∈ {RootVariantScaleRef(root_degree, variant), SubVScaleRef(target_degree)}`
- `A ⊆ D` 为和弦内部组成级位集合，且必须包含 `Degrees.I`

因此，`ChordId` 的作用不是给和弦命名，  
而是给出“如何在一个调式中构造该和弦”的索引说明。

在当前实现中，调式 `mode` 的公开入口有以下几类：

1. `mode[scale_ref]`
2. `ChordId`
3. `mode.chord(scale_ref, composition=None)`

其含义分别是：

第一，若给出 `mode[scale_ref]`，  
则直接返回该 `scale_ref` 规范化后的目标音阶。

第二，若给出 `ChordId(scale_ref, A)`，  
则先由 `mode` 根据 `scale_ref` 解析出目标音阶，  
再以该音阶和组成集合 `A` 构造和弦。

第三，若给出 `mode.chord(scale_ref, A)`，  
则把 `scale_ref` 作为显式入口送入统一的 canonical 解析流程。  
若 `A` 省略，则按 `Chord` 的默认组成规则生成和弦。

因此，调式索引和弦的本质可以写作：

```text
mode[scale_ref] = mode[canonical_scale_ref]
mode[ChordId(scale_ref, A)] = Chord(mode[canonical_scale_ref], A)
```

这说明，在本包中，调式对音阶与和弦的索引都不是查表行为，  
而是一个“显式 scale_ref -> canonical scale_ref -> scale/chord”的构造过程。

<a id="section-3-11"></a>
### 3.11 最小用例

下面这个例子把调式这一章最关键的三条入口放在一起：

1. `mode[scale_ref]` 入口
2. `mode.chord(scale_ref, ...)` 入口
3. canonicalization

```python
from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.enums.core import Degrees, NoteNames
from composer_theory.domain.enums.harmony import Modes, VariantForm
from composer_theory.domain.ids import RootVariantScaleRef, SubVScaleRef
from composer_theory.domain.mode import Mode

mode = Mode(BaseNote(NoteNames.C), Modes.Dorian)

scale = mode[RootVariantScaleRef(Degrees.II, VariantForm.Base)]
triad = mode.chord(RootVariantScaleRef(Degrees.II, VariantForm.Base))
minor7 = mode.chord(
    RootVariantScaleRef(Degrees.II, VariantForm.Base),
    frozenset({Degrees.I, Degrees.III, Degrees.V, Degrees.VII}),
)
subv = mode.chord(SubVScaleRef(Degrees.VI), frozenset({Degrees.I, Degrees.III, Degrees.VII}))

assert str(scale) == "D, E, F, G, A, B, C"
assert str(triad) == "Dmin"
assert str(minor7) == "Dmin7"
assert str(mode[SubVScaleRef(Degrees.I)]) == "Db, Eb, F, Gb, Ab, Bb, Cb"
```

---

<a id="chapter-4"></a>
## 第四章 调性

本章对应文件：

- `domain/ids.py`
- `domain/key.py`

<a id="section-4-1"></a>
### 4.1 调性的基本定义

调性对应 `Key`。  
一个调性由两项构成：

```text
K = (t, m0)
```

其中：

- `t` 为主音；
- `m0` 为主调式类型。

因此，调性在本包中的作用，不是重新定义全部音，  
而是为调式提供一个统一的高层上下文。

<a id="section-4-2"></a>
### 4.2 调性的主调式

给定调性 `K = (t, m0)`，  
则其主调式就是以主音 `t` 和调式类型 `m0` 构造的调式。

因此，调性并不是脱离调式独立存在的对象，  
而是建立在一个主调式之上的更高层结构。

<a id="section-4-3"></a>
### 4.3 调性中的同主音入口

若在调性 `K` 中直接用某个调式类型 `m` 取值，  
则得到的是与主音相同、但调式类型不同的调式。

这类入口对应 `ModeAccess.Substitute`。

因此，这一入口保留的是主音不变，只改变调式类型。

<a id="section-4-4"></a>
### 4.4 调性中的关系调式入口

若在调性 `K` 中用某个音级 `r ∈ D` 取值，  
则得到的是主调式第 `r` 级所导出的关系调式。

这类入口对应 `ModeAccess.Relative`。

因此，这一入口保留的是“同一主调式体系中的级位派生关系”。

<a id="section-4-5"></a>
### 4.5 调性与 SubV 的边界

当前实现中，`Key` 不再直接提供 `SubV` 入口。  
`Key` 只负责生成普通 `Mode` 上下文；  
`SubV` 被下移为 `Mode` 内部的一种音阶解析规则。

也就是说，当前结构更接近：

```text
key -> mode -> scale_ref -> chord
```

其中 `SubVScaleRef(target_degree)` 的规则现在是：

1. 先在当前 `Mode` 的基础音阶上取 `target_degree` 对应的目标音；
2. 用该目标音上方的小二度作为 `subv` 主音，按当前 `ModeSpec.subv_profile` 构造目标 degree 的 `subv` 音阶；
3. 直接返回这个结果，不再额外做第二次旋转。

也就是说，只有显式配置了 `ModeSpec.subv_profile` 的调式才支持 `Mode[SubVScaleRef(...)]`。
若某个调式未配置 `subv_profile`，则访问 `SubVScaleRef(...)` 会报“不支持 SubV”。

<a id="section-4-6"></a>
### 4.6 调性的模式空间

从结构上看，一个调性并不是单独一个调式，  
而是一个允许若干入口方式的模式空间。

它至少包含：

1. 同主音调式集合；
2. 关系调式集合。

因此，调性的意义不在于“只给出主调”，  
而在于给出一个可以枚举内部模式来源的理论环境。

<a id="section-4-7"></a>
### 4.7 调性的反查

调性还可以对模式、音阶、基音、和弦做反查。  
其意义是：

给定某个对象，判断它是否可以在该调性的某个入口中被解释。

因此，调性既能正向生成模式，  
也能反向判定某个对象在自身结构中的归属。

<a id="section-4-8"></a>
### 4.8 调性编号

为了使“一个调性”本身也能被结构化标识，  
本包定义了 `KeyId`。

一个 `KeyId` 由两部分组成：

```text
KID = (tonic, main_mode_type)
```

其中：

- `tonic ∈ N`
- `main_mode_type ∈ Modes`

这表示：

一个调性的身份，  
由主音名称与主调式类型共同确定。

因此，`KeyId` 的作用不是参与调性内部索引，  
而是为“哪一个调性”提供一个稳定编号。

换言之：

- `KeyId` 负责标识调性对象本身；
- `ModeId` 负责标识调性内部的调式入口；
- `ChordId` 负责标识调式内部的和弦入口。

由此可见，本包中的 ID 系统具有明确层级：

```text
KeyId
-> ModeId
-> ChordId
```

这说明，编号体系和理论对象的构造层级是一致的。

<a id="section-4-9"></a>
### 4.9 调性索引与调式编号

为了使“调性索引调式”成为统一操作，  
本包定义了 `ModeId`。

一个 `ModeId` 由两部分组成：

```text
MID = (role, access)
```

其中：

- `role ∈ Modes ∪ D`
- `access ∈ {Substitute, Relative}`

这里的含义是：

第一，`role` 表示被访问对象所依附的角色。  
它可以是某个调式类型，也可以是某个音级。

第二，`access` 表示访问路径。  
也就是说，同一个 `role` 必须结合访问方式，才能确定应当如何从调性生成目标调式。

在当前实现中，调性 `key` 可以接受以下四类索引：

1. `Modes`
2. `Degrees`
3. `(Degrees, ModeAccess)`
4. `ModeId`

其含义分别是：

第一，若用某个 `Modes` 成员索引，  
则保持主音不变，只改变调式类型。  
这对应同主音访问。

第二，若用某个 `Degrees` 成员索引，  
则取主调式基础音阶的该级为新主音，  
再按主调式与该级的关系推导目标调式类型。  
这对应关系调式访问。

第三，若用 `(degree, access)` 索引，  
则按显式访问方式生成目标调式。  
其中当前特别支持：

- `(degree, Relative)`

第四，若用 `ModeId(role, access)` 索引，  
则把上述几类访问方式统一编码成一个结构化编号。

因此，调性索引调式的本质不是“从容器中取现成对象”，  
而是：

```text
key[ModeId(role, access)] = 按访问规则构造的 Mode
```

这说明，在本包中，`ModeId` 承担的是“调性内部模式入口编号”的作用。

<a id="section-4-10"></a>
### 4.10 最小用例

下面这个例子展示调性的三种常用索引方式：

```python
from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.enums.core import Degrees, NoteNames
from composer_theory.domain.enums.harmony import ModeAccess, Modes
from composer_theory.domain.ids import ModeId
from composer_theory.domain.key import Key

key = Key(BaseNote(NoteNames.C), Modes.Ionian)

c_dorian = key[Modes.Dorian]
d_dorian = key[Degrees.II]
same_as_type = key[ModeId(role=Modes.Dorian, access=ModeAccess.Substitute)]

assert str(c_dorian) == "C-Dorian"
assert str(d_dorian) == "D-Dorian"
assert same_as_type == c_dorian
```

---

<a id="part-relations"></a>
## 关系解析篇

本篇对应下列代码文件：

- `relations/__init__.py`
- `relations/hit.py`
- `relations/tools.py`
- `relations/chord_in_mode.py`
- `relations/mode_in_key.py`
- `relations/chord_in_key.py`
- `resolve/resolver.py`

本篇只讨论公开接口。  
所谓公开接口，是指：

1. `relations.__all__` 中导出的关系命中对象；
2. 各命中对象上不以下划线开头的属性与方法；
3. `Resolver.resolve(...)` 这一统一解析入口。

因此，本篇不把 `_ensure_*`、`_color_shift`、`_altered_degrees` 一类内部计算函数当作文档主体。

从结构上说，关系层的任务不是“重新定义和弦、调式、调性”，  
而是回答以下三类问题：

1. 一个和弦如何被某个调式解释；
2. 一个调式如何被某个调性解释；
3. 一个和弦如何被某个调性解释。

---

<a id="chapter-5"></a>
## 第五章 关系层的公开对象

<a id="section-5-1"></a>
### 5.1 导出集合

`composer_theory.relations` 当前公开导出四个名称：

- `ResolveHit`
- `ChordInModeHit`
- `ModeInKeyHit`
- `ChordInKeyHit`

因此，关系层对外的基本单位不是“布尔判断”，  
而是“命中对象”。

<a id="section-5-2"></a>
### 5.2 命中的一般形式

设 `x` 与 `y` 为两个乐理对象。  
若系统能够把 `x` 在 `y` 的上下文中加以解释，则返回一个命中对象 `hit`。

因此，在本包中，解析结果不写作：

```text
True / False
```

而写作：

```text
hit = 某种 ResolveHit 子类
```

这表示：  
系统关注的不是“能不能解释”这一件事，  
而是“以什么身份被解释、附带哪些分析结果、属于哪一种关系类型”。

<a id="section-5-3"></a>
### 5.3 命中的共同特征

所有命中对象都继承自 `ResolveHit`。  
当前 `ResolveHit` 自身不提供专门字段，  
它的作用是：

1. 作为关系命中对象的共同父类型；
2. 提供统一的字符串表示入口。

因此，`ResolveHit` 在本包中是一个抽象上的类型边界，  
而不是一个承载分析值的实体对象。

<a id="section-5-4"></a>
### 5.4 公开属性与内部属性的边界

关系层对象上的公开属性，表示用户可以直接依赖的结果。  
例如：

- `is_member`
- `function_scores`
- `chromatic_score`
- `color`

而以下划线开头的成员，表示内部推导过程。  
这些成员只用于：

1. 延迟计算；
2. 缓存；
3. 中间结构变换；
4. 支撑公开结果。

因此，在使用关系层时，应把公开属性理解为“结果层”，  
把私有成员理解为“实现层”。

<a id="section-5-5"></a>
### 5.5 最小用例

关系层最简单的读取方式，不是直接 new 某个 hit，  
而是交给 `Resolver` 返回合适的命中对象：

```python
from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.enums.core import Degrees, NoteNames
from composer_theory.domain.enums.harmony import Modes
from composer_theory.domain.key import Key
from composer_theory.relations import ModeInKeyHit
from composer_theory.resolve.resolver import Resolver

key = Key(BaseNote(NoteNames.C), Modes.Ionian)
hits = Resolver().resolve(key[Degrees.II], key)

assert hits
assert isinstance(hits[0], ModeInKeyHit)
assert hits[0].is_member is True
```

---

<a id="chapter-6"></a>
## 第六章 `ChordInModeHit`

<a id="section-6-1"></a>
### 6.1 所表示的关系

`ChordInModeHit` 表示：

```text
Chord ∈ Mode
```

也就是说，它描述的是：  
一个和弦如何在某个调式中被解释。

<a id="section-6-2"></a>
### 6.2 基本字段

一个 `ChordInModeHit` 由以下公开字段确定：

- `mode`
- `chord_id`
- `chord`

其中：

- `mode` 表示被解释所依附的调式；
- `chord_id` 表示该和弦若属于此调式，则它在该调式中的身份；
- `chord` 表示被分析的实际和弦对象。

因此，一个 `ChordInModeHit` 的核心不是“这个和弦本身是什么”，  
而是“这个和弦在此调式里被看作什么”。

<a id="section-6-3"></a>
### 6.3 成员命中与非成员命中

设 `hit` 为一个 `ChordInModeHit`。  
则：

- 当 `hit.chord_id is not None` 时，称该命中为成员命中；
- 当 `hit.chord_id is None` 时，称该命中为非成员命中。

公开属性 `is_member` 正是对此事实的直接表达。

因此，在本包中，和弦对调式的解析并不只允许“命中或空”。  
即使该和弦不属于该调式，也可以返回一个非成员分析命中。

<a id="section-6-4"></a>
### 6.4 和弦身份

若 `hit.chord_id` 存在，则它包含三项：

- `scale_ref`
- 和弦内部组成 `composition`

其中 `scale_ref` 可能有两种形式：

- `RootVariantScaleRef(root_degree, variant)`
- `SubVScaleRef(target_degree)`

这两项共同决定：

该和弦在此调式中，  
是按普通 root+variant 方式解释，还是按 `SubV` 方式解释，  
并由哪些相对级位构成。

因此，`chord_id` 不是“和弦名字”，  
而是调式内部的一种定位坐标。

成员命中的和弦组成与是否为 `SubV`，也应当直接从 `chord_id` 读取。  
也就是说，只有当 `hit.is_member is True` 时，才应继续读取：

- `hit.chord_id.composition`
- `hit.chord_id.is_subv`

<a id="section-6-5"></a>
### 6.5 功能分数

`hit.function_scores` 返回一个从和声功能到分数的映射：

```text
Functions -> float
```

当前至少包括：

- `Tonic`
- `Dominant`
- `Subdominant`

其意义是：  
把该和弦的组成音，放到当前调式主音为参考点的坐标下，  
统计它对各功能证据的匹配程度。

因此，`function_scores` 不是和弦固有属性，  
而是“和弦相对当前调式”的功能分析结果。

<a id="section-6-6"></a>
### 6.6 半音化分数

`hit.chromatic_score` 表示该和弦相对当前调式基础形态所产生的半音化程度。

若该命中是：

1. 非成员命中，则统计和弦中有多少音不属于该调式基础音阶；
2. 基础形态成员命中，则分数为 `0`；
3. 非基础形态成员命中，则统计该和弦涉及的级位中，有多少级相对基础形态发生了偏移。

因此，`chromatic_score` 描述的是该和弦相对调式基础骨架的离调程度。

<a id="section-6-7"></a>
### 6.7 色彩结果

`hit.color` 的结果为：

```text
(Transition, ColorShift)
```

其中：

- 第一项描述和弦质量与根音的变化；
- 第二项描述所属音阶结构的色彩变化。

因此，在关系层中，色彩结果不是单独一个标签，  
而是和弦差与音阶差的联合表达。

<a id="section-6-8"></a>
### 6.8 转折点

`hit.turning_points` 返回一个集合。  
它只在以下条件下可能非空：

1. 当前命中是成员命中；
2. 当前命中的 `scale_ref` 为 `RootVariantScaleRef`；
3. 当前命中的 `variant` 不是 `Base`；
4. 该和弦涉及到与 `VI`、`VII` 相关的关注级位。

因此，转折点不是每个和弦都天然携带的标签，  
而是特定 root+variant 形态下由级位组合触发的运行时结果。  
`SubVScaleRef` 命中默认不产生 turning point。

<a id="section-6-9"></a>
### 6.9 字符串表示

`str(hit)` 会给出一条面向阅读的关系说明。  
若为非成员命中，则强调其是 `non-member analysis`；  
若为成员命中，则会写出根级、组成级与形态信息。

因此，字符串表示的作用不是替代字段访问，  
而是把一条命中压缩成可快速浏览的说明文本。

<a id="section-6-10"></a>
### 6.10 最小用例

下面这个例子展示一个标准成员命中：

```python
from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.enums.core import Degrees, NoteNames
from composer_theory.domain.enums.harmony import Modes, VariantForm
from composer_theory.domain.ids import ChordId, RootVariantScaleRef
from composer_theory.domain.mode import Mode
from composer_theory.relations import ChordInModeHit
from composer_theory.resolve.resolver import Resolver

mode = Mode(BaseNote(NoteNames.C), Modes.Ionian)
chord = mode[
    ChordId(
        RootVariantScaleRef(Degrees.V, VariantForm.Base),
        frozenset({Degrees.I, Degrees.III, Degrees.V, Degrees.VII}),
    )
]
hit = Resolver().resolve(chord, mode)[0]

assert isinstance(hit, ChordInModeHit)
assert hit.is_member is True
assert hit.chord_id.scale_ref == RootVariantScaleRef(Degrees.V, VariantForm.Base)
assert hit.turning_points == set()
```

---

<a id="chapter-7"></a>
## 第七章 `ModeInKeyHit`

<a id="section-7-1"></a>
### 7.1 所表示的关系

`ModeInKeyHit` 表示：

```text
Mode ∈ Key
```

也就是说，它描述的是：  
一个调式如何在某个调性中被解释。

<a id="section-7-2"></a>
### 7.2 基本字段

一个 `ModeInKeyHit` 由以下公开字段确定：

- `key`
- `mode_id`
- `mode`
- `is_member`

其中：

- `key` 表示被解释所依附的调性；
- `mode_id` 表示该调式在调性中的入口身份；
- `mode` 表示被命中的具体调式对象。

因此，`ModeInKeyHit` 所回答的问题是：  
这个调式在该调性中属于哪一种入口，而不是单纯地“是否相等”。

<a id="section-7-3"></a>
### 7.3 成员命中与直接分析命中

设 `hit` 为一个 `ModeInKeyHit`。  
则：

- 当 `hit.mode_id is not None` 时，称该命中为成员命中；
- 当 `hit.mode_id is None` 时，称该命中为直接分析命中。

公开属性 `is_member` 正是对此事实的直接表达。

因此，在当前实现中，调式对调性的解析也允许回退分析。  
即使一个调式不能作为该调性的明确入口被命中，  
系统仍可以返回一个 `ModeInKeyHit` 来承载功能与色彩分析结果。

<a id="section-7-4"></a>
### 7.4 调式身份

`mode_id` 由两部分组成：

- `access`
- `role`

其中：

- `access` 指示入口类型；
- `role` 指示该入口所依附的角色。

当前入口类型包括：

- `Substitute`
- `Relative`

因此，调式在调性中的身份并不只有一种。  
同一个调式可以通过不同入口被纳入同一调性环境。

<a id="section-7-5"></a>
### 7.5 功能分数

`hit.function_scores` 返回：

```text
Functions -> float
```

它所分析的对象不是该调式中的任意和弦，  
而是该调式主和弦骨架在主调式参考系下的功能证据。

因此，这个分数描述的是：  
该调式一旦被放入此调性，  
其骨架重心更偏向主功能、属功能还是下属功能。

<a id="section-7-6"></a>
### 7.6 半音化分数

`hit.chromatic_score` 表示：

相对于主调式基础形态，  
该调式基础形态中共有多少个音级发生了变音。

因此，这个量不是统计“有几个外来音实例”，  
而是统计“有几个结构级位与主调骨架不同”。

若该命中不是成员命中，  
则当前实现改为直接比较：

1. 当前调式基础音阶的七个级位；
2. 主调式基础音阶的音高类集合。

此时它表示的是：  
该调式基础音阶中，有多少个级位的音高类不属于主调式音高集合。

<a id="section-7-7"></a>
### 7.7 色彩结果

`hit.color` 仍写作：

```text
(Transition, ColorShift)
```

但这里所比较的对象不是任意和弦，  
而是：

1. 当前调式的骨架主和弦；
2. 调性主调式的主和弦。

因此，`ModeInKeyHit.color` 表达的是：

当一个调式被纳入某个调性时，  
它相对于主调中心所带来的功能色彩位移。

<a id="section-7-8"></a>
### 7.8 字符串表示

`str(hit)` 会写出：

- 调式名；
- 入口类型；
- 入口角色；
- 所属调性。

若该命中不是成员命中，则会写成该调式在某调性中的直接分析。

因此，字符串表示提供的是一条“调式在调性中的归属句子”。

<a id="section-7-9"></a>
### 7.9 最小用例

下面这个例子展示一个关系调式命中：

```python
from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.enums.core import Degrees, NoteNames
from composer_theory.domain.enums.harmony import ModeAccess, Modes
from composer_theory.domain.ids import ModeId
from composer_theory.domain.key import Key
from composer_theory.relations import ModeInKeyHit
from composer_theory.resolve.resolver import Resolver

key = Key(BaseNote(NoteNames.C), Modes.Ionian)
mode = key[Degrees.II]
hit = Resolver().resolve(mode, key)[0]

assert isinstance(hit, ModeInKeyHit)
assert hit.is_member is True
assert hit.mode_id == ModeId(role=Degrees.II, access=ModeAccess.Relative)
assert hit.mode == mode
```

---

<a id="chapter-8"></a>
## 第八章 `ChordInKeyHit`

<a id="section-8-1"></a>
### 8.1 所表示的关系

`ChordInKeyHit` 表示：

```text
Chord ∈ Key
```

也就是说，它描述的是：  
一个和弦如何在某个调性中被解释。

<a id="section-8-2"></a>
### 8.2 复合结构

`ChordInKeyHit` 不是从零开始的单层关系。  
它内部包含：

- 一个 `ModeInKeyHit`
- 一个可能存在的 `ChordId`
- 一个实际和弦 `chord`

因此，它本质上是两层解释的叠加：

```text
Chord ∈ Mode ∈ Key
```

<a id="section-8-3"></a>
### 8.3 公开字段

一个 `ChordInKeyHit` 当前公开以下核心字段与属性：

- `mode_in_key_hit`
- `chord_id`
- `chord`
- `is_member`
- `function_scores`
- `chromatic_score`
- `color`

这说明，`ChordInKeyHit` 对外保留的是完整复合关系本身，  
而不再额外摊平内部上下文。

<a id="section-8-4"></a>
### 8.4 调式成员性

`is_member` 表示：

该和弦是否至少可以作为某个调式内部和弦，  
从而经由该调式进入当前调性。

因此，它不是“是否属于这个调性”的绝对布尔值，  
而是“是否属于当前解释链条中的调式成员”。

<a id="section-8-5"></a>
### 8.5 上下文读取方式

若需要读取该命中所依附的调性与调式上下文，  
则应显式通过 `mode_in_key_hit` 进入。

例如，应当读取：

- `hit.mode_in_key_hit.key`
- `hit.mode_in_key_hit.mode`
- `hit.mode_in_key_hit.mode_id`

因此，`ChordInKeyHit` 不再把这些上下文信息额外摊平成自身属性。

若需要读取成员命中的和弦身份细节，也应当显式通过 `chord_id` 进入。  
也就是说，只有当 `hit.is_member is True` 时，才应继续读取：

例如，应当读取：

- `hit.chord_id.composition`
- `hit.chord_id.is_subv`

<a id="section-8-6"></a>
### 8.6 功能分数

`hit.function_scores` 返回一个功能分数字典。  
它的参考系不是当前被命中的调式主音，  
而是当前调性的主调式主音。

因此，这个分数所回答的问题是：

该和弦若放在整个调性中心下看，  
更像主、属还是下属。

<a id="section-8-7"></a>
### 8.7 半音化分数

`hit.chromatic_score` 当前按主调式基础音阶统计外来音高类数量。

也就是说，系统先取当前调性的主调式基础音阶，  
再看该和弦中有多少音高类不在其中。

因此，`ChordInKeyHit` 的半音化分数关注的是：

该和弦相对“主调中心”的离调程度，  
而不是相对其局部命中调式的离调程度。

<a id="section-8-8"></a>
### 8.8 色彩结果

`hit.color` 仍返回：

```text
(Transition, ColorShift)
```

但其比较基准是：

1. 当前和弦；
2. 当前调性主调式的主和弦。

因此，它描述的是：  
该和弦相对于调性中心主和弦的综合位移。

<a id="section-8-9"></a>
### 8.9 成员命中与直接分析命中

与 `ChordInModeHit` 类似，  
`ChordInKeyHit` 也允许 `chord_id` 为空。

当 `chord_id is None` 时，  
表示系统没有找到一个具体的调式内成员身份，  
但仍然返回一个基于当前调性的直接分析命中。

因此，在本包中，`Chord ∈ Key` 的解析也不是简单的“命中或空”，  
而保留了一种调性层面的回退分析结果。

<a id="section-8-10"></a>
### 8.10 字符串表示

`str(hit)` 会在成员命中时写出：

- 调式
- 入口类型
- 入口角色
- 普通命中时的 root/variant，或 `SubV` 命中时的 target
- 组成级

若为直接分析命中，则直接写成该和弦在某调性中的直接分析。

因此，字符串表示压缩的是一条完整的复合解释路径。

<a id="section-8-11"></a>
### 8.11 最小用例

下面这个例子展示一个典型的 `Chord ∈ Key` 成员命中：

```python
from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.enums.core import Degrees, NoteNames
from composer_theory.domain.enums.harmony import ModeAccess, Modes, VariantForm
from composer_theory.domain.ids import ChordId, RootVariantScaleRef
from composer_theory.domain.key import Key
from composer_theory.relations import ChordInKeyHit
from composer_theory.resolve.resolver import Resolver

key = Key(BaseNote(NoteNames.C), Modes.Ionian)
mode = key[Degrees.I]
chord = mode[
    ChordId(
        RootVariantScaleRef(Degrees.V, VariantForm.Base),
        frozenset({Degrees.I, Degrees.III, Degrees.V, Degrees.VII}),
    )
]
hit = Resolver().resolve(chord, key)[0]

assert isinstance(hit, ChordInKeyHit)
assert hit.is_member is True
assert hit.mode_in_key_hit.mode_id.access == ModeAccess.Substitute
assert hit.chord_id.scale_ref == RootVariantScaleRef(Degrees.V, VariantForm.Base)
```

---

<a id="chapter-9"></a>
## 第九章 `Resolver`

<a id="section-9-1"></a>
### 9.1 统一解析入口

`Resolver` 的公开入口是：

```python
resolve(a, b) -> List[AnyResolveHit]
```

其中 `AnyResolveHit` 是以下三类命中的并集：

- `ChordInModeHit`
- `ModeInKeyHit`
- `ChordInKeyHit`

因此，解析器的任务不是返回单个固定类型，  
而是根据输入对象对，返回对应关系域中的命中列表。

<a id="section-9-2"></a>
### 9.2 支持的输入对

当前解析器支持三类输入：

1. `Chord, Mode`
2. `Mode, Key`
3. `Chord, Key`

若用户输入顺序反过来，  
解析器会在内部判断是否可以交换次序后再继续处理。

因此，解析器对这三类关系采用的是“有向关系定义 + 有限交换兼容”的策略。

<a id="section-9-3"></a>
### 9.3 `Chord -> Mode` 的解析

当输入为 `Chord` 与 `Mode` 时，  
解析器会遍历该调式的全部可用 `scale_ref` 候选。

若某一候选满足：

1. 该 `scale_ref` 所解析出的音阶可以承载当前和弦组成；
2. 构造出的候选和弦与输入和弦具有相同基音集合；

则生成一个 `ChordInModeHit`。

当前枚举的候选包括：

1. 各个 `RootVariantScaleRef(root_degree, variant)`；
2. 各个 `SubVScaleRef(target_degree)`；

命中后还会经过 canonicalization 去重。

若所有形态都失败，  
则仍返回一个 `ChordInModeHit`，但令：

- `chord_id = None`
- `chord = 原始和弦`

因此，`Chord -> Mode` 解析始终至少返回一个分析结果。

<a id="section-9-4"></a>
### 9.4 `Mode -> Key` 的解析

当输入为 `Mode` 与 `Key` 时，  
解析器会依次检查：

1. 同主音入口；
2. 关系调式入口。

凡是能与输入调式相等者，都生成一个 `ModeInKeyHit`。

若没有任何入口命中，  
则仍返回一个 `ModeInKeyHit`，但令：

- `mode_id = None`
- `mode = 原始调式`

因此，`Mode -> Key` 现在也保留了回退分析机制。  
它与另外两条解析链一样，都会至少返回一个分析结果。

<a id="section-9-5"></a>
### 9.5 `Chord -> Key` 的解析

当输入为 `Chord` 与 `Key` 时，  
解析器会先枚举该调性的全部模式入口。

对于每一个模式入口，  
它先构造 `ModeInKeyHit`，  
再尝试把该和弦精确解析为该模式中的成员和弦。  
每当精确命中成功，就生成一个 `ChordInKeyHit`。

若全部入口都不能得到成员命中，  
则解析器仍返回一个 `ChordInKeyHit`，其中：

- `chord_id = None`
- `chord = 原始和弦`

同时，它仍附带一个默认的 `ModeInKeyHit` 作为调性上下文。

因此，`Chord -> Key` 也保留了回退分析机制。

<a id="section-9-6"></a>
### 9.6 返回值的意义

解析器返回的是列表，而不是单个命中。  
这是因为：

1. 一个对象可能通过多个入口被解释；
2. 一个和弦可能在多个形态中都成立；
3. 一个调式可能以多种方式纳入同一调性。

因此，解析结果天然允许多义性，  
而不是强制压缩为唯一答案。

<a id="section-9-7"></a>
### 9.7 最小用例

下面这个例子把三条解析链放在一起：

```python
from composer_theory.domain.base_note import BaseNote
from composer_theory.domain.enums.core import Degrees, NoteNames
from composer_theory.domain.enums.harmony import Modes, VariantForm
from composer_theory.domain.ids import ChordId, RootVariantScaleRef
from composer_theory.domain.key import Key
from composer_theory.relations import ChordInKeyHit, ChordInModeHit, ModeInKeyHit
from composer_theory.resolve.resolver import Resolver

resolver = Resolver()
key = Key(BaseNote(NoteNames.C), Modes.Ionian)
mode = key[Degrees.I]
chord = mode[
    ChordId(
        RootVariantScaleRef(Degrees.V, VariantForm.Base),
        frozenset({Degrees.I, Degrees.III, Degrees.V, Degrees.VII}),
    )
]

hits_chord_mode = resolver.resolve(chord, mode)
hits_mode_key = resolver.resolve(key[Degrees.II], key)
hits_chord_key = resolver.resolve(chord, key)

assert any(isinstance(hit, ChordInModeHit) for hit in hits_chord_mode)
assert any(isinstance(hit, ModeInKeyHit) for hit in hits_mode_key)
assert any(isinstance(hit, ChordInKeyHit) for hit in hits_chord_key)
```

---

## 本文档小结

本文档由两篇组成。

第一篇说明 `domain` 层的基础乐理定义。  
第二篇说明 `relations` 与 `resolve` 层如何把和弦、调式、调性组织成可解析的关系系统。

在关系层中，系统不直接返回真假值，  
而是返回命中对象。  
每个命中对象都同时携带：

1. 关系身份；
2. 上下文对象；
3. 功能分析结果；
4. 半音化结果；
5. 色彩结果。

在解析层中，`Resolver` 统一负责把对象对映射成命中列表。  
其中：

- `Chord -> Mode` 有非成员回退分析；
- `Mode -> Key` 有直接分析回退；
- `Chord -> Key` 有调性层回退分析。

因此，`composer_theory` 在当前结构下，不只是一个静态乐理对象集合，  
也是一个可以对“和弦、调式、调性之间的解释关系”进行形式化求解的系统。
