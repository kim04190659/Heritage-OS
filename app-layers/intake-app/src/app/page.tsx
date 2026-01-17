"use client";

import { useState } from "react";

export default function IntakeForm() {
  const [formData, setFormData] = useState({
    title: "",
    sourceType: "field_log",
    capturedBy: "",
    rawText: "",
  });
  const [status, setStatus] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("Saving...");

    try {
      const res = await fetch("/api/save-log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (res.ok) {
        setStatus("Success! Log saved to Archive.");
        setFormData({ ...formData, title: "", rawText: "" });
      } else {
        setStatus("Error saving log.");
      }
    } catch (err) {
      console.error(err);
      setStatus("Network Error.");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-8 font-sans">
      <div className="max-w-2xl mx-auto bg-white shadow-xl rounded-lg p-6">
        <header className="mb-6 border-b pb-4">
          <h1 className="text-2xl font-bold text-slate-800">
            Heritage-OS Intake
          </h1>
          <p className="text-slate-500">現場暗黙知・リアルタイム収集ツール</p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700">
              タイトル (事象・件名)
            </label>
            <input
              type="text"
              required
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border focus:ring-blue-500 focus:border-blue-500"
              placeholder="例: 〇〇地区 住民説明会の反応"
              value={formData.title}
              onChange={(e) =>
                setFormData({ ...formData, title: e.target.value })
              }
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700">
                ソース種別
              </label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border"
                value={formData.sourceType}
                onChange={(e) =>
                  setFormData({ ...formData, sourceType: e.target.value })
                }
              >
                <option value="field_log">現場メモ (Field Log)</option>
                <option value="interview_audio">インタビュー記録</option>
                <option value="handwritten_note">手書きメモ解読</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">
                記録者ID
              </label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border"
                placeholder="Staff ID"
                value={formData.capturedBy}
                onChange={(e) =>
                  setFormData({ ...formData, capturedBy: e.target.value })
                }
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700">
              暗黙知・コンテキスト
              <span className="ml-2 text-xs text-gray-400">
                ※判断の背景や感情を含めて記述
              </span>
            </label>
            <textarea
              required
              rows={6}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-3 border focus:ring-blue-500 focus:border-blue-500"
              placeholder="住民は当初怒りを見せていたが、我々が『過去の経緯』に触れた瞬間、表情が和らいだ。判断の決め手は..."
              value={formData.rawText}
              onChange={(e) =>
                setFormData({ ...formData, rawText: e.target.value })
              }
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 transition font-bold"
          >
            アーカイブへ保存
          </button>

          {status && (
            <div
              className={`mt-4 p-3 rounded ${status.includes("Success") ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}
            >
              {status}
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
