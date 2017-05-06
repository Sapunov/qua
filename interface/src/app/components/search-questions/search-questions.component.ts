import 'rxjs/add/operator/switchMap';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { NgProgressService } from 'ng2-progressbar';

import { QuestionService } from '../../services/question.service';
import { IQuestion, IQuestions, IQuestionsParams } from '../../interfaces/question.interface';

@Component({
  selector: 'app-search-questions',
  templateUrl: './search-questions.component.html',
  styleUrls: ['./search-questions.component.less']
})
export class SearchQuestionsComponent implements OnInit {
  questions: IQuestions;
  items: IQuestion[];
  url: string;
  prevResult: string;
  nextResult: string;

  constructor(
    private route: ActivatedRoute,
    private questionService: QuestionService,
    private pbService: NgProgressService,
    private router: Router
  ) {
    this.prevResult = null;
    this.nextResult = null;
    this.items = [];
    this.url = '/questions';
  }

  ngOnInit() {
    this.route.queryParams
      .switchMap((params: IQuestionsParams) => {
        this.pbService.start();
        window.scrollTo(0, 0);
        return this.questionService.getQuestions(params)
          .catch(err => {
            this.pbService.done();
          });
      })
      .subscribe((questions: IQuestions) => {
        if (questions) {
          this.pbService.done();
          this.questions = questions;
          this.items = questions.items;
          this.prevResult = questions.pagination.prev;
          this.nextResult = questions.pagination.next;
        }
      });
  }
}
