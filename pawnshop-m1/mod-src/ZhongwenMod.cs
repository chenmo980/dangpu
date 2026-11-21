using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using HarmonyLib;

// Pawnshop CN M1 - ASCII-only assembly; CN strings load from names.json at runtime
[HarmonyPatch(typeof(LocHelper), "GetLocalizedItem")]
public static class ZhongwenNamePatch
{
    public static Dictionary<string, string> Names = new Dictionary<string, string>();
    public static bool Loaded;

    public static void Postfix(string key, ref string __result)
    {
        if (!Loaded || key == null) return;
        string zh;
        if (Names.TryGetValue(key, out zh)) __result = zh;
    }
}

public class ZhongwenMod : IMod
{
    const char BSLASH = (char)92;

    public void Init(ModManifest manifest)
    {
        try
        {
            string modDir = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Mods", "ZhongwenM1");
            string path = System.IO.Path.Combine(modDir, "names.json");
            string json = File.ReadAllText(path, Encoding.UTF8);
            var raw = MiniJson.Parse(json) as Dictionary<string, object>;
            if (raw != null)
            {
                foreach (var kv in raw)
                {
                    if (kv.Value is string s) ZhongwenNamePatch.Names[kv.Key] = s;
                }
                ZhongwenNamePatch.Loaded = true;
                UnityEngine.Debug.Log("[ZhongwenMod] Init OK: " + ZhongwenNamePatch.Names.Count + " entries");
                string test = LocHelper.GetLocalizedItem("item_beis_icecream_name");
                UnityEngine.Debug.Log("[ZhongwenMod] self-test => " + test);
            }
            else UnityEngine.Debug.Log("[ZhongwenMod] names.json parse failed");
        }
        catch (Exception e)
        {
            UnityEngine.Debug.Log("[ZhongwenMod] Init error: " + e.Message);
        }
    }
    public void OnEnable() { UnityEngine.Debug.Log("[ZhongwenMod] OnEnable"); }
    public void OnDisable() { UnityEngine.Debug.Log("[ZhongwenMod] OnDisable"); }
}

public static class MiniJson
{
    const char BSL = (char)92;
    public static object Parse(string json)
    {
        int pos = 0;
        return ParseValue(json, ref pos);
    }
    static object ParseValue(string s, ref int pos)
    {
        SkipWs(s, ref pos);
        if (pos >= s.Length) return null;
        char c = s[pos];
        if (c == '{') return ParseObj(s, ref pos);
        if (c == '[') return ParseArr(s, ref pos);
        if (c == '"' + BSL + '"') return null;   // defensive
        if (c == '"') return ParseStr(s, ref pos);
        int start = pos;
        while (pos < s.Length && (",}]".IndexOf(c) < 0)) { pos++; }
        return s.Substring(start, pos - start).Trim();
    }
    static void SkipWs(string s, ref int pos){ while (pos < s.Length && char.IsWhiteSpace(s[pos])) pos++; }
    static Dictionary<string, object> ParseObj(string s, ref int pos)
    {
        var obj = new Dictionary<string, object>();
        pos++; SkipWs(s, ref pos);
        if (pos < s.Length && s[pos] == '}') { pos++; return obj; }
        while (pos < s.Length)
        {
            SkipWs(s, ref pos);
            string k = ParseStr(s, ref pos);
            SkipWs(s, ref pos);
            pos++;
            obj[k] = ParseValue(s, ref pos);
            SkipWs(s, ref pos);
            if (pos < s.Length && s[pos] == ',') { pos++; continue; }
            if (pos < s.Length && s[pos] == '}') { pos++; break; }
        }
        return obj;
    }
    static string ParseStr(string s, ref int pos)
    {
        pos++;
        var sb = new System.Text.StringBuilder();
        while (pos < s.Length)
        {
            char c = s[pos++];
            if (c == '"') break;
            if (c == BSL)
            {
                char n = s[pos++];
                if (n == 'n') sb.Append((char)10);
                else if (n == 't') sb.Append((char)9);
                else if (n == 'r') sb.Append((char)13);
                else if (n == '"') sb.Append('"');
                else if (n == BSL) sb.Append(BSL);
                else if (n == 'u')
                {
                    sb.Append((char)Convert.ToInt32(s.Substring(pos, 4), 16));
                    pos += 4;
                }
                continue;
            }
            sb.Append(c);
        }
        return sb.ToString();
    }
    static List<object> ParseArr(string s, ref int pos)
    {
        var arr = new List<object>();
        pos++; SkipWs(s, ref pos);
        while (pos < s.Length)
        {
            SkipWs(s, ref pos);
            if (pos < s.Length && s[pos] == ']') { pos++; break; }
            arr.Add(ParseValue(s, ref pos));
            SkipWs(s, ref pos);
            if (pos < s.Length && s[pos] == ',') { pos++; continue; }
            if (pos < s.Length && s[pos] == ']') { pos++; break; }
        }
        return arr;
    }
}
