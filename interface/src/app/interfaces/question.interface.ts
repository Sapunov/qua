export interface IUser {
  first_name: string;
  id: number;
  last_name: string;
  username: string;
}

export interface IAnswer {
  created_at: string;
  created_by: IUser;
  html: string;
  id: number;
  raw: string;
  updated_at: string;
  updated_by: {
      first_name: string;
      id: number;
      last_name: string;
      username: string;
  };
  version: number;
}

export interface IQuestion {
  answer?: IAnswer;
  answer_exists?: boolean;
  created_at: string;
  created_by: IUser;
  id: number;
  keywords: string[];
  title: string;
  updated_at: string;
  updated_by: IUser;
}

export interface IQuestions {
  items: IQuestion[];
  total: number;
  pagination: {
    next: string | null;
    prev: string | null;
  };
}
export interface INewQuestion {
  answer?: {
    raw?: string;
  };
  keywords?: string[];
  title: string;
}

export interface ITempQuestion {
  question?: IQuestion;
  answer: string;
  keywords: string[];
  title: string;
  id: number;
}

export interface IQuestionsParams {
  offset: string;
  limit: string;
}
