import { Subject } from 'rxjs/Subject';
import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions, URLSearchParams } from '@angular/http';
import { URLS, MIN_CHARS_FOR_SEARCH } from '../../environments/const';

import 'rxjs/add/operator/toPromise';

import { ErrorService } from './error.service';

import { ISearchResult, ISearchInfo } from '../interfaces/search-hits.interface';
import { IResponse } from '../interfaces/response.interface';

@Injectable()
export class SearchService {
  searchInfo = new Subject<ISearchInfo>();
  searchInfo$ = this.searchInfo.asObservable();
  private prevResult: string;
  private nextResult: string;

  constructor(
    private errorService: ErrorService,
    private http: Http
  ) {
    this.prevResult = '';
    this.nextResult = '';
  }

  goSearch(query: string, spelling?: string): Promise<ISearchResult> {
    query = query || '';

    if (query.length < MIN_CHARS_FOR_SEARCH) {
      this.searchInfo.next(null);
      return Promise.resolve({
        query,
        total: 0,
        hits: []
      } as ISearchResult);
    }
    let options = this.makeOptions();
    let param: URLSearchParams = new URLSearchParams;
    param.set('query', query);
    param.set('offset', '0');
    param.set('limit', '10');
    if (typeof spelling !== 'undefined' && spelling === '0') {
      param.set('spelling', spelling.toString());
    }
    options.search = param;
    return this.http.get(`${URLS.search}`, options)
      .toPromise()
      .then(this.promiseHandler)
      .then((result: ISearchResult) => {
        this.prevResult = result.pagination.prev;
        this.nextResult = result.pagination.next;
        this.searchInfo.next({
          total: result.total,
          took: result.took
        });
        return result;
      })
      .catch(this.errorHandler);
  }

  loadNextResult(): Promise<ISearchResult> {
    if (!this.nextResult) {
      return Promise.resolve(null);
    }
    let options = this.makeOptions();
    let url = this.nextResult;
    this.nextResult = null;
    return this.http.get(`${url}`, options)
      .toPromise()
      .then(this.promiseHandler)
      .then((result: ISearchResult) => {
        this.prevResult = result.pagination.prev;
        this.nextResult = result.pagination.next;
        return result;
      })
      .catch(this.errorHandler);
  }

  private makeOptions() {
    let headers =  new Headers({
      'Content-type': 'application/json',
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
