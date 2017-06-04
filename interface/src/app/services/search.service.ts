import { Subject } from 'rxjs/Subject';
import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions, URLSearchParams } from '@angular/http';
import { URLS, MIN_CHARS_FOR_SEARCH, ITEM_LIMIT, ITEM_OFFSET } from '../../environments/const';

import 'rxjs/add/operator/toPromise';

import { ErrorService } from './error.service';

import { ISearchResult, ISearchInfo, ISearchParams, ISuggest, IGetSuggests } from '../interfaces/search-hits.interface';
import { IResponse } from '../interfaces/response.interface';

@Injectable()
export class SearchService {
  searchInfo = new Subject<ISearchInfo>();
  searchInfo$ = this.searchInfo.asObservable();

  constructor(
    private errorService: ErrorService,
    private http: Http
  ) {

  }

  getSuggests(params: IGetSuggests): Promise<ISuggest[] | null> {
    let query = params.query || '';

    if (query.length < MIN_CHARS_FOR_SEARCH) {
      this.searchInfo.next(null);
      return Promise.resolve(null);
    }

    let options = this.makeOptions();
    let param: URLSearchParams = new URLSearchParams;

    param.set('query', query);
    param.set('limit', params.limit);

    options.search = param;

    return this.http.get(`${URLS.suggests}`, options)
      .toPromise()
      .then(this.promiseHandler)
      .then((result: ISuggest[]) => result)
      .catch(this.errorHandler);
  }

  goSearch(params: ISearchParams): Promise<ISearchResult | null> {
    let query = params.query || '';

    if (query.length < MIN_CHARS_FOR_SEARCH) {
      this.searchInfo.next(null);
      return Promise.resolve(null);
    }
    let options = this.makeOptions();
    let param: URLSearchParams = new URLSearchParams;
    param.set('query', query);
    param.set('offset', params.offset || ITEM_OFFSET);
    param.set('limit', params.limit || ITEM_LIMIT);
    if (typeof params.spelling !== 'undefined' && params.spelling === '0') {
      param.set('spelling', params.spelling.toString());
    }
    options.search = param;
    return this.http.get(`${URLS.search}`, options)
      .toPromise()
      .then(this.promiseHandler)
      .then((result: ISearchResult) => {
        this.searchInfo.next({
          total: result.total,
          took: result.took
        });
        return result;
      })
      .catch(this.errorHandler);
  }

  private makeOptions() {
    let headers =  new Headers({
      Authorization: `JWT ${localStorage.getItem('token')}`
    });
    let options = new RequestOptions({
      headers: headers,
      withCredentials: true
    });
    return options;
  }

  private promiseHandler = (res: any): any => {
    let response = res.json() as IResponse;
    if (!response.ok) {
      throw response.error;
    }
    return response.response;
  }

  private errorHandler = (error) => {
    return this.errorService.handleError(error);
  }
}
