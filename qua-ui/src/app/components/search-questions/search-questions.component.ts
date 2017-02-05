import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NgProgressService } from 'ng2-progressbar';

import { QuestionService } from '../../services/question.service';
import { IQuestion, IQuestions } from '../../interfaces/question.interface';

@Component({
  selector: 'app-search-questions',
  templateUrl: './search-questions.component.html',
  styleUrls: ['./search-questions.component.less']
})
export class SearchQuestionsComponent implements OnInit {
  questions: IQuestions;
  items: IQuestion[];

  constructor(
    private questionService: QuestionService,
    private pbService: NgProgressService,
    private router: Router
  ) {
    this.items = [];
  }

  getQuestion(id: number) {
    this.router.navigate([`questions/${id}`]);
  }

  onScrollDown() {
    this.questionService.loadNextItems()
      .then(questions => {
        if (questions) {
          this.items = this.items.concat(questions.items);
        }
      });
  }

  ngOnInit() {
    if (this.questionService.questions) {
      this.questions = this.questionService.questions;
    } else {
      this.pbService.start();
      this.questionService.getQuestions()
        .then((questions: IQuestions) => {
          this.pbService.done();
          this.questions = questions;
          this.items = questions.items;
        })
        .catch(err => {
          this.pbService.done();
        });
    }
  }
}
