import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import { v4 as uuidv4 } from "uuid";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { title, sourceType, rawText, capturedBy, location } = body;

    if (!title || !rawText) {
      return NextResponse.json(
        { error: "Title and content are required" },
        { status: 400 },
      );
    }

    const id = uuidv4();
    const timestamp = new Date().toISOString();

    // Map to Knowledge Schema
    const logData = {
      id,
      title,
      created_at: timestamp,
      source_metadata: {
        type: sourceType || "field_log",
        captured_by: capturedBy || "Anonymous Staff",
        location: location || {},
        tags_at_capture: [],
      },
      content: {
        raw_text: rawText,
        summary: "",
        file_url: "",
      },
      git_metadata: {
        // Placeholder for initial state
        file_path: "",
        status: "draft",
      },
    };

    // Path to save: knowledge-assets/raw-logs
    // Assuming the app is running in app-layers/intake-app, we go up 3 levels
    const saveDir = path.resolve(
      process.cwd(),
      "../../knowledge-assets/raw-logs",
    );

    // Ensure dir exists
    if (!fs.existsSync(saveDir)) {
      fs.mkdirSync(saveDir, { recursive: true });
    }

    const filePath = path.join(saveDir, `log-${id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(logData, null, 2), "utf-8");

    return NextResponse.json({ success: true, id, filePath });
  } catch (error) {
    console.error("Save Error:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 },
    );
  }
}
