// Shapes of the API's request and response bodies. Field names match the
// server exactly (snake_case), because these are the JSON keys it sends.

export interface Tool {
  id: number;
  name: string;
  category: string;
  description: string;
  loan_period_days: number;
  available: boolean;
}

export interface Member {
  id: number;
  name: string;
  email: string;
  joined_date: string;
}

export interface Loan {
  id: number;
  tool_id: number;
  member_id: number;
  borrowed_date: string;
  due_date: string;
  returned_date: string | null;
}

export interface ToolsResponse {
  tools: Tool[];
}

export interface ToolResponse {
  tool: Tool;
}

export interface MembersResponse {
  members: Member[];
}

export interface LoansResponse {
  loans: Loan[];
}

// Every error response from the server has this shape.
export interface ApiErrorBody {
  detail: string;
}
