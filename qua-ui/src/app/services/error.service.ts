import { Subject } from 'rxjs/Subject';
import { Injectable } from '@angular/core';

import { IError } from '../interfaces/error.interface';
import { IResponse } from '../interfaces/response.interface';

@Injectable()
export class ErrorService {
  private error = new Subject<IError>();

  error$ = this.error.asObservable();

  constructor() { }

  viewError(err: IError) {
    console.error(err);
    this.error.next(err);
  }

  handleError(response: any) {
    let res = response.json() as IResponse;
    if (!res.ok) {
      return Promise.reject(res.error);
    }
  }
}
