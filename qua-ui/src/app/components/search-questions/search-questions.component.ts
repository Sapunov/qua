import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { QuestionService } from '../../services/question.service';
import { ErrorService } from '../../services/error.service';
import { IQuestion } from '../../interfaces/question.interface';

@Component({
  selector: 'app-search-questions',
  templateUrl: './search-questions.component.html',
  styleUrls: ['./search-questions.component.less']
})
export class SearchQuestionsComponent implements OnInit {
  questions: IQuestion[] = [];

  constructor(
    private errorService: ErrorService,
    private questionService: QuestionService,
    private router: Router
  ) { }

  getQuestion(id: number) {
    this.router.navigate([`questions/${id}`]);
  }

  ngOnInit() {
    this.questionService.getQuestions()
      .then((questions: IQuestion[]) => {
        this.questions = questions;
      })
      .catch(err => this.errorService.viewError(err));
  }

}
