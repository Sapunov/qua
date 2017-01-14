import { IUser } from './question.interface';

export interface ICategory {
  created_at: string;
  created_by: IUser;
  id: number;
  name: string;
  updated_at: string;
  updated_by: IUser;
}
