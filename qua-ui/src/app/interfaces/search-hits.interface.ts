import { ICat } from './category.interface';

export interface IHits {
  id: number;
  title: string;
  snippet: string;
  image: string;
  score: number;
  keywords: string[];
  categories: ICat[];
  url_params: {
    qid: number;
    shid: number;
    token: string;
  }
}

export interface ICategoryAssumptions {
  id: number;
  name: string;
  score: number;
}

export interface ISearchResult {
  query: string;
  hits: IHits[];
  total: number;
  category_assumptions: ICategoryAssumptions[];
};
