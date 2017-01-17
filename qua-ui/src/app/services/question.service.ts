import 'rxjs/add/operator/toPromise';
import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions, URLSearchParams } from '@angular/http';
import { URLS } from '../../environments/const';

import { INewQuestion, IQuestion } from '../interfaces/question.interface';
import { IResponse } from '../interfaces/response.interface';

@Injectable()
export class QuestionService {
  public question: IQuestion | INewQuestion;
  private headers = new Headers({
    'Content-type': 'application/json',
    Authorization: `JWT ${localStorage.getItem('token')}`
  });

  constructor(private http: Http) { }

  editQuestion(id: number, data: INewQuestion): Promise<IQuestion> {
    let options = new RequestOptions({
      headers: this.headers,
      withCredentials: true
    });
    return this.http.put(`${URLS.question}/${id}`, JSON.stringify(data), options)
      .toPromise()
      .then((response: any) => {
        return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        if (!response.ok) {
          throw response.error;
        }
        return response.response;
      })
      .catch(this.handleError);
  }
  addQuestion(data: INewQuestion): Promise<IQuestion> {
    let options = new RequestOptions({
      headers: this.headers,
      withCredentials: true
    });
    return this.http.post(URLS.question, JSON.stringify(data), options)
      .toPromise()
      .then((response: any) => {
        return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        if (!response.ok) {
          throw response.error;
        }
        return response.response;
      })
      .catch(this.handleError);
  }

  getQuestion(urlParams): Promise<IQuestion> {
    let options = new RequestOptions({
      headers: this.headers,
      withCredentials: true,
    });
    let keysQueryParam = Object.keys(urlParams.queryParams);
    let queryParams = new URLSearchParams();
    keysQueryParam.forEach((key: string) => {
      queryParams.set(key, urlParams.queryParams[key]);
    });
    options.search = queryParams;
    return this.http.get(`${URLS.question}/${urlParams.params.id}`, options)
      .toPromise()
      .then((response: any) => {
          return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        if (!response.ok) {
          throw response.error;
        }
        return response.response;
      })
      .catch(this.handleError);
  }

  getQuestions(): Promise<IQuestion[]> {
    let options = new RequestOptions({
      headers: this.headers,
      withCredentials: true,
    });
    return this.http.get(`${URLS.question}`, options)
      .toPromise()
      .then((response: any) => {
          return response.json() as IResponse;
      })
      .then((response: IResponse) => {
        if (!response.ok) {
          throw response.error;
        }
        return response.response as IQuestion[];
      })
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }
}
