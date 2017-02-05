import 'rxjs/add/operator/toPromise';
import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions, URLSearchParams } from '@angular/http';
import { URLS } from '../../environments/const';

import { ErrorService } from './error.service';

import { INewQuestion, IQuestion } from '../interfaces/question.interface';
import { IResponse } from '../interfaces/response.interface';

@Injectable()
export class QuestionService {
  public question: INewQuestion;
  public questions: IQuestion[];

  constructor(
    private errorService: ErrorService,
    private http: Http) {
    this.question = null;
    this.questions = null;
    }

  addQuestion(data: INewQuestion): Promise<IQuestion> {
    let options = this.makeOptions();
    return this.http.post(URLS.question, JSON.stringify(data), options)
      .toPromise()
      .then(this.promiseHandler)
      .catch(this.errorHandler);
  }

  editQuestion(id: number, data: INewQuestion): Promise<IQuestion> {
    let options = this.makeOptions();
    return this.http.put(`${URLS.question}/${id}`, JSON.stringify(data), options)
      .toPromise()
      .then(this.promiseHandler)
      .catch(this.errorHandler);
  }

  deleteQuestion(id: number): Promise<boolean> {
    let options = this.makeOptions();
    let index = this.searchQuestionById(id);
    if (index !== -1) {
      this.questions.splice(index, 1);
    }
    return this.http.delete(`${URLS.question}/${id}`, options)
      .toPromise()
      .then(this.promiseHandler)
      .catch(this.errorHandler);
  }

  getQuestion(urlParams): Promise<IQuestion> {
    let options = this.makeOptions();
    let keysQueryParam = Object.keys(urlParams.queryParams);
    let queryParams = new URLSearchParams();
    keysQueryParam.forEach((key: string) => {
      queryParams.set(key, urlParams.queryParams[key]);
    });
    options.search = queryParams;
    return this.http.get(`${URLS.question}/${urlParams.params.id}`, options)
      .toPromise()
      .then(this.promiseHandler)
      .catch(this.errorHandler);
  }

  getQuestions(): Promise<IQuestion[]> {
    let options = this.makeOptions();
    return this.http.get(`${URLS.question}`, options)
      .toPromise()
      .then(this.promiseHandler)
      .then((questions: IQuestion[]) => this.questions = questions)
      .catch(this.errorHandler);
  }

  clearCacheQuestions() {
    this.questions = null;
  }

  private searchQuestionById(id): number {
    let index = -1;
    if (!this.questions) {
      return index;
    }
    this.questions.forEach((question, i) => {
      if (question.id === id) {
        index = i;
      }
    });
    return index;
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
