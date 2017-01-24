import { Subscription }   from 'rxjs/Subscription';
import { Component, OnInit, OnDestroy } from '@angular/core';

import { ErrorService } from '../../services/error.service';
import { IError } from '../../interfaces/error.interface';


@Component({
  selector: 'app-error',
  templateUrl: './error.component.html',
  styleUrls: ['./error.component.less']
})
export class ErrorComponent implements OnInit, OnDestroy {
  errors: IError[] = [];
  sub: Subscription;

  constructor(
    private errorService: ErrorService
  ) { }

  ngOnInit() {
    this.sub = this.errorService.error$.subscribe((err: IError) => {
      if (typeof err.error_msg !== 'string') {
        err.error_msg = 'Неизвестная ошибка, смотрите консоль';
      }
      this.errors.push(err);
      setTimeout(() => {
        this.errors.shift();
      }, 5000);
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
