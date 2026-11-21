# ZhongwenMod 构建说明

## 模组格式（逆向自 ModLoader.cs）
- 位置：游戏根目录 `Mods/<模组名>/`
- `manifest.xml`：ID/Name/Author/ModVersion/Description/Assemblies（相对 DLL 路径）
- DLL 必须实现 `IMod` 接口（Init/OnEnable/OnDisable）
- Loader 自动：Assembly.LoadFrom → 找 IMod 实现 → Harmony(id=mod.ID).PatchAll → Init → OnEnable

## 编译（引用游戏自带 BCL，无外部依赖）
```
dotnet "<Unity Editor>/Editor/Data/DotNetSdkRoslyn/csc.dll" -noconfig -nostdlib+ -nologo ^
  -target:library -out:ZhongwenMod.dll @refs.rsp ZhongwenMod.cs
```
refs.rsp 引用（游戏 Managed 目录）：mscorlib.dll(netstandard.dll)/System.dll/System.Core.dll/Assembly-CSharp.dll/UnityEngine.CoreModule.dll/0Harmony.dll

## ⚠ 两个已踩的坑
1. **中文字符串不能进 DLL 元数据**——Harmony 初始化在 GBK 系统编码下读模组程序集会报
   "Illegal byte sequence"（哪怕路径/名字是 ASCII，元数据里的中文也会触发）。
   解法：中文字典放 names.json（UTF-8），运行时 File.ReadAllText(Encoding.UTF8) 加载。
2. **游戏路径不能含中文**——HarmonySharedState.cctor → Assembly.GetCodeBase() 在中文路径下同错误。
   解法：游戏放纯 ASCII 路径（如 C:\PawnshopTest\）。

## 安装
游戏根目录 Mods/ZhongwenM1/：manifest.xml + ZhongwenMod.dll + names.json
游戏内 Mods 菜单启用（或 SaveFile.es3 的 modOrder 键预写 ["zhongwen.m1"]）
