export interface IHits {
  id: number;
  title: string;
  snippet: string;
  image: string;
  score: number;
  category: {
    id: number
    name: string;
  };
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
