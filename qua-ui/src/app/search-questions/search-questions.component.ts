import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router'

import { QuestionService } from '../question.service';
import { IQuestion } from '../question.interface';

@Component({
  selector: 'app-search-questions',
  templateUrl: './search-questions.component.html',
  styleUrls: ['./search-questions.component.less']
})
export class SearchQuestionsComponent implements OnInit {
  questions: IQuestion[] = [];

  constructor(
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
  }

}
