import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/mergeMap';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';
import { Location } from '@angular/common';

import { QuestionService } from '../question.service';
import { IQuestion } from '../question.interface';

@Component({
  selector: 'app-search-question',
  templateUrl: './search-question.component.html',
  styleUrls: ['./search-question.component.less']
})
export class SearchQuestionComponent implements OnInit {
  question: IQuestion;
  raw: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private Location: Location,
    private questionService: QuestionService
  ) { }

  edit() {
    let params: NavigationExtras = {
      skipLocationChange: true,
      queryParams: {
        title: this.question.title,
        answer: this.question.answer.raw,
        keywords: this.question.keywords,
        categories: this.question.categories,
        id: this.question.id,
        reply: true
      }
    };
    this.router.navigate(['add'], params);
  }
  reply() {
    let params: NavigationExtras = {
      skipLocationChange: true,
      queryParams: {
        title: this.question.title,
        keywords: this.question.keywords,
        categories: this.question.categories,
        id: this.question.id,
        reply: true
      }
    };
    this.router.navigate(['add'], params);
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
        return this.questionService.getQuestion(allParams);
      })
      .subscribe((result: IQuestion) => {
        this.question = result;
        this.raw = result.answer ? result.answer.raw : '';
        return result;
      });
  }
}
