import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/mergeMap';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';
import { Location } from '@angular/common';
import { NgProgressService } from 'ng2-progressbar';

import { ErrorService, QuaError } from '../../services/error.service';
import { QuestionService } from '../../services/question.service';
import { IQuestion, INewQuestion } from '../../interfaces/question.interface';

@Component({
  selector: 'app-search-question',
  templateUrl: './search-question.component.html',
  styleUrls: ['./search-question.component.less']
})
export class SearchQuestionComponent implements OnInit {
  question: IQuestion;
  raw: string;

  constructor(
    private errorService: ErrorService,
    private route: ActivatedRoute,
    private router: Router,
    private Location: Location,
    private pbService: NgProgressService,
    private questionService: QuestionService
  ) {
  }

  edit() {
    this.questionService.question = this.question;
    this.router.navigate(['edit']);
  }

  delete() {
    if (!confirm('Вы уверены, что хотите удалить этот вопрос?')) {
      return;
    }
    let id = this.question.id;
    if (id) {
      this.pbService.start();
      this.questionService.deleteQuestion(id)
        .then(() => {
          this.pbService.done();
          this.router.navigate(['questions']);
        })
        .catch(err => {
          this.pbService.done();
        });
    } else {
      this.errorService.viewError(new QuaError({
        error_msg: `Question ${id} is not found`
      }));
    }
  }

  ngOnInit() {
    let allParams: any = {};
    this.pbService.start();
    this.route.params
      .switchMap((params: Params) => {
        allParams.params = params;
        return this.route.queryParams;
      })
      .switchMap((params: Params) => {
        allParams.queryParams = params;
        return this.questionService.getQuestion(allParams)
          .catch(err => null);
      })
      .subscribe((result: IQuestion) => {
        this.pbService.done();
        if (result) {
          this.question = result;
          this.raw = result.answer ? result.answer.raw : '';
          return result;
        }
      });
  }
}
