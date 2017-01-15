import 'rxjs/add/operator/switchMap';
import { Component, OnInit, OnDestroy, ViewChild  } from '@angular/core';
import { ActivatedRoute, Params, Router, NavigationExtras } from '@angular/router';

import { MarkdownComponent } from '../markdown/markdown.component';

import { QuestionService } from '../question.service';
import { CategoryService } from '../category.service';

import { IQuestion, INewQuestion, ICategories } from '../question.interface';
import { ICategory } from '../category.interface';

@Component({
  selector: 'app-search-add',
  templateUrl: './search-add.component.html',
  styleUrls: ['./search-add.component.less']
})
export class SearchAddComponent implements OnInit, OnDestroy {
  @ViewChild(MarkdownComponent) private mde: MarkdownComponent;

  question: INewQuestion | IQuestion;
  allCategories: ICategories[];
  isReply: boolean = false;
  sfHide: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private questionService: QuestionService,
    private categoryService: CategoryService
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
      categories: this.question.categories,
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
      categories: this.question.categories,
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

  getCategories() {
    this.categoryService.getCategories()
      .then((categories: ICategory[]) => {
        this.allCategories = categories;
      });
  }

  addCategory(index: number) {
    this.question.categories.push({
      id: this.allCategories[index].id,
      name: this.allCategories[index].name
    });
  }

  delCategory(index: number) {
    this.question.categories.splice(index, 1);
  }

  addKeyword(keyword: string) {
    if (keyword) {
      this.question.keywords.push(keyword);
    }
  }

  delKeyword(index: number) {
    this.question.keywords.splice(index, 1);
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
    this.getCategories();
  }

  ngOnDestroy() {
    this.questionService.question = null;
  }
}
