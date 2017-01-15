import 'rxjs/add/operator/switchMap';
import { Component, OnInit, OnDestroy, ViewChild  } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';

import { MarkdownComponent } from '../markdown/markdown.component';

import { QuestionService } from '../question.service';

import { IQuestion, INewQuestion } from '../question.interface';

@Component({
  selector: 'app-search-add',
  templateUrl: './search-add.component.html',
  styleUrls: ['./search-add.component.less']
})
export class SearchAddComponent implements OnInit, OnDestroy {
  @ViewChild(MarkdownComponent) private mde: MarkdownComponent;

  question: INewQuestion | IQuestion;
  isReply: boolean = false;
  sfHide: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private questionService: QuestionService
  ) {  }

  onSubmit(question: string): void {
    let raw: string = this.mde.getValue();
    if (this.isReply) {
      this.edit(this.question['id'], question, raw);
    } else {
      this.add(question, raw);
    }
  }

  edit(id: number, title: string, raw: string) {
    let data: INewQuestion = {
      title,
      keywords: this.question.keywords,
      answer: {
        raw
      }
    };
    this.questionService.editQuestion(id, data)
      .then((que: IQuestion) => {
        this.router.navigate([`questions/${que.id}`]);
      });
  }

  add(title: string, raw: string) {
    let data: INewQuestion = {
      title,
      keywords: this.question.keywords,
      answer: {
        raw
      }
    };
    this.questionService.addQuestion(data)
      .then((que: IQuestion) => {
        this.router.navigate([`questions/${que.id}`]);
      });
  }

  addKeyword(keyword: string) {
    if (keyword) {
      this.question.keywords.push(keyword);
    }
  }

  ngOnInit() {
    let question: IQuestion | INewQuestion = this.questionService.question;
    if (question) {
      question.keywords = question.keywords || [];
      question.categories = question.categories || [];
      question.answer = question.answer ? question.answer : { raw: '' };
      this.isReply = question.reply;
      this.question = question;
    } else {
      this.question = {
        title: '',
        answer: {
          raw: ''
        },
        categories: [],
        keywords: []
      } as INewQuestion;
    }
  }

  ngOnDestroy() {
    this.questionService.question = null;
  }
}
