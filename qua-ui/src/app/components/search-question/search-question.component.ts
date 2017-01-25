import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/mergeMap';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';
import { Location } from '@angular/common';

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
  loading: boolean;
  raw: string;

  constructor(
    private errorService: ErrorService,
    private route: ActivatedRoute,
    private router: Router,
    private Location: Location,
    private questionService: QuestionService
  ) {
    this.loading = false;
  }

  edit() {
    this.questionService.question = this.question;
    this.loading = true;
    this.router.navigate(['add']);
  }

  delete() {
    if (!confirm('Вы уверены, что хотите удалить этот вопрос?')) {
      return;
    }
    let id = this.question.id;
    if (id) {
      this.loading = true;
      this.questionService.deleteQuestion(id)
        .then(() => {
          this.loading = false;
          this.router.navigate(['questions']);
        })
        .catch(err => {
          this.loading = false;
        });
    } else {
      this.errorService.viewError(new QuaError({
        error_msg: `Question ${id} is not found`
      }));
    }
  }

  ngOnInit() {
    let allParams: any = {};
    this.loading = true;
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
        this.loading = false;
        if (result) {
          this.question = result;
          this.raw = result.answer ? result.answer.raw : '';
          return result;
        }
      });
  }
}
