export interface IResponse {
  ok: number;
  response?: any;
  error?: {
    error_code: number;
    error_msg: string;
  };
}
