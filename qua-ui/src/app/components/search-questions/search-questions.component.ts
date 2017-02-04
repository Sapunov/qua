import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NgProgressService } from 'ng2-progressbar';

import { QuestionService } from '../../services/question.service';
import { IQuestion } from '../../interfaces/question.interface';

@Component({
  selector: 'app-search-questions',
  templateUrl: './search-questions.component.html',
  styleUrls: ['./search-questions.component.less']
})
export class SearchQuestionsComponent implements OnInit {
  questions: IQuestion[] = [];

  constructor(
    private questionService: QuestionService,
    private pbService: NgProgressService,
    private router: Router
  ) {
  }

  getQuestion(id: number) {
    this.router.navigate([`questions/${id}`]);
  }

  ngOnInit() {
    if (this.questionService.questions) {
      this.questions = this.questionService.questions;
    } else {
      this.pbService.start();
      this.questionService.getQuestions()
        .then((questions: IQuestion[]) => {
          this.pbService.done();
          this.questions = questions;
        })
        .catch(err => {
          this.pbService.done();
        });
    }
  }
}
