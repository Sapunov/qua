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
  version: 2;
}

export interface ICategories {
  id: number;
  name: string;
}

export interface IQuestion {
  answer: IAnswer;
  categories: ICategories[];
  created_at: string;
  created_by: IUser;
  id: number;
  keywords: string[];
  title: string;
  updated_at: string;
  updated_by: IUser;
}

export interface INewQuestion {
  reply?: boolean;
  answer?: {
    raw?: string;
    snippet?: string;
  };
  categories?: number[];
  keywords?: string[];
  title: string;
}
