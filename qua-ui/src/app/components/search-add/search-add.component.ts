import 'rxjs/add/operator/switchMap';
import { Component, OnInit, OnDestroy, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';
import { FormGroup } from '@angular/forms';
import { NgProgressService } from 'ng2-progressbar';

import { MarkdownComponent } from '../markdown/markdown.component';

import { QuestionService } from '../../services/question.service';

import { IQuestion, INewQuestion, IAnswer } from '../../interfaces/question.interface';

@Component({
  selector: 'app-search-add',
  templateUrl: './search-add.component.html',
  styleUrls: ['./search-add.component.less']
})
export class SearchAddComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild(MarkdownComponent) private mde: MarkdownComponent;
  @ViewChild('inputTitle') private inputTitle: ElementRef;

  sfHide: boolean;
  isEdit: boolean;
  question: IQuestion;
  title: string;
  keywords: string[];
  keyword: string;
  answer: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private questionService: QuestionService,
    private pbService: NgProgressService,
  ) {
    this.sfHide = true;
    this.isEdit = false;
    this.title = '';
    this.keyword = '';
    this.keywords = [];
    this.answer = {
      raw: ''
    };
  }

  onSubmit(form: FormGroup): void {
    if (form.invalid) {
      return;
    }
    let data: INewQuestion = {
      title: this.title,
      keywords: this.keywords,
      answer: { raw: this.mde.getValue() }
    };
    if (this.isEdit) {
      this.edit(this.question.id, data);
    } else {
      this.add(data);
    }
  }

  onBackspace(event: KeyboardEvent) {
    if (this.keywords.length && !this.keyword) {
      this.keywords.pop();
    }
  }

  edit(id: number, data: INewQuestion) {
    this.pbService.start();
    this.questionService.editQuestion(id, data)
      .then((que: IQuestion) => {
        this.pbService.done();
        this.router.navigate([`questions/${que.id}`]);
      })
      .catch(err => {
        this.pbService.done();
      });
  }

  add(data: INewQuestion) {
    this.pbService.start();
    this.questionService.addQuestion(data)
      .then((que: IQuestion) => {
        this.pbService.done();
        this.router.navigate([`questions/${que.id}`]);
      })
      .catch(err => {
        this.pbService.done();
      });
  }

  addKeyword() {
    let checkKeywords = this.keywords.indexOf(this.keyword);
    if (this.keyword && checkKeywords) {
      this.keywords.push(this.keyword);
    }
  }

  delKeyword(keyword: string) {
    let index = this.keywords.indexOf(keyword);
    if (index !== -1) {
      this.keywords.splice(index, 1);
    }
  }

  ngOnInit() {
    let question = this.questionService.question;
    if (question) {
      this.title = question.title || this.title;
      this.keywords = question.keywords ? question.keywords.slice() : this.keywords;
      this.answer = question.answer ? Object.assign({}, question.answer) : this.answer;
      this.question = question as IQuestion;
      this.isEdit = this.question.id ? true : false;
    }
  }

  ngAfterViewInit() {
    this.inputTitle.nativeElement.focus();
  }

  ngOnDestroy() {
    this.questionService.question = null;
  }
}
