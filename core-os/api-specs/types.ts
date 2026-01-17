export type SourceType =
  | "interview_audio"
  | "video"
  | "handwritten_note"
  | "existing_document"
  | "field_log";
export type KnowledgeStatus = "draft" | "review" | "published" | "archived";

export interface LocationData {
  latitude?: number;
  longitude?: number;
  place_name?: string;
}

export interface SourceMetadata {
  type: SourceType;
  captured_by?: string;
  location?: LocationData;
  tags_at_capture?: string[];
}

export interface ContentData {
  raw_text?: string;
  summary?: string;
  file_url?: string;
}

export interface AiAnalysisData {
  judgment_logic?: string;
  emotional_context?: string;
  legal_basis?: string;
  risk_factors?: string[];
  tags?: string[];
}

export interface GitMetadata {
  file_path: string;
  last_commit_hash?: string;
  status: KnowledgeStatus;
}

/**
 * Heritage Knowledge Artifact
 * Represents a single unit of captured knowledge within the Heritage-OS.
 */
export interface KnowledgeArtifact {
  id: string; // UUID
  title: string;
  created_at: string; // ISO 8601
  updated_at?: string; // ISO 8601

  source_metadata: SourceMetadata;
  content: ContentData;

  // AI-enriched fields correspond to Feature #3 (Context Engine)
  ai_analysis?: AiAnalysisData;

  // Sync metadata corresponds to Feature #4 (GitHub Mirroring)
  git_metadata: GitMetadata;
}
