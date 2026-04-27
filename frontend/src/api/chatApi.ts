import apiClient from './client';

export interface ChatApiRequest {
  message: string;
  current_draft?: Record<string, any>;
}

export interface ChatApiResponse {
  reply: string;
  // The backend packages the draft, missing_fields, and uncertain_fields into this payload
  interaction_draft: Record<string, any>; 
}

/**
 * Sends a natural language message to the backend LangGraph workflow.
 * 
 * @param payload The user's chat message and the current interaction draft state.
 * @returns The agent's textual response alongside the updated deterministic UI state.
 */
export const sendChatMessage = async (payload: ChatApiRequest): Promise<ChatApiResponse> => {
  const response = await apiClient.post<ChatApiResponse>('/chat/', payload);
  return response.data;
};
