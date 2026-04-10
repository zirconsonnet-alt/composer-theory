# `composer-theory`

`composer-theory` 是一个面向 Python 的独立乐理对象与关系解析库。

它提供：

- 基础乐理对象：`BaseNote`、`Scale`、`Quality`、`Chord`、`Mode`、`Key`
- 关系命中对象：`ChordInModeHit`、`ModeInKeyHit`、`ChordInKeyHit`
- 统一解析入口：`Resolver`

## 快速入口

- PyPI：<https://pypi.org/project/composer-theory/>
- 完整文档：[composer_theory/README.md](./composer_theory/README.md)
- API 文档：[composer_theory/API.md](./composer_theory/API.md)
- Issues：<https://github.com/zirconsonnet-alt/composer-theory/issues>

## 安装

```bash
pip install composer-theory
```

## API 总览

### `composer_theory.domain`

- `BaseNote`
- `Scale`
- `ColorShift`
- `Resolution`
- `DissonanceRelation`
- `EdgeRule`
- `SetRule`
- `KeyId`
- `ModeId`
- `RootVariantScaleRef`
- `SubVScaleRef`
- `ChordId`
- `Transition`
- `ModeSpec`
- `Quality`
- `Chord`
- `Mode`
- `Key`

### `composer_theory.domain.enums`

- `Degrees`
- `NoteNames`
- `Intervals`
- `Qualities`
- `Modes`
- `VariantForm`
- `Tonality`
- `ChromaticType`
- `Functions`
- `ModeAccess`
- `DynamicType`
- `DegreeVariant`
- `TurningPoints`
- `States`
- `Voices`
- `LeadingType`
- `Textures`

### `composer_theory.relations` / `composer_theory.resolve`

- `ResolveHit`
- `ModeInKeyHit`
- `ChordInModeHit`
- `ChordInKeyHit`
- `Resolver`

### `composer_theory.implement`

- `Note`
- `Arrangement`

完整签名、公开属性、公开方法，以及 `[]` / `|` / `+` / `-` 等协议说明见 [composer_theory/API.md](./composer_theory/API.md)。
