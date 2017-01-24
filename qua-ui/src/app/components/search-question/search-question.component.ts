import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/mergeMap';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';
import { Location } from '@angular/common';

import { ErrorService } from '../../services/error.service';
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
    this.router.navigate(['add']);
  }

  delete() {
    let id = this.question.id;
    if (this.loading) {
      return;
    }
    if (id) {
      this.loading = true;
      this.questionService.deleteQuestion(id)
        .then(() => {
          this.router.navigate(['questions']);
        })
        .catch(err => this.errorService.viewError(err))
        .then(() => {
          this.loading = false;
        });
    } else {
      this.errorService.viewError({
        error_msg: `Question ${id} is not found`
      });
    }
  }

  ngOnInit() {
    let allParams: any = {};
    this.route.params
      .switchMap((params: Params) => {
        allParams.params = params;
        return this.route.queryParams;
      })
      .switchMap((params: Params) => {
        allParams.queryParams = params;
        return this.questionService.getQuestion(allParams)
          .catch(err => this.errorService.viewError(err));
      })
      .subscribe((result: IQuestion) => {
        if (result) {
          this.question = result;
          this.raw = result.answer ? result.answer.raw : '';
          return result;
        }
      });
  }
}
