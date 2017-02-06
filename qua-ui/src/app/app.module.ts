import { BrowserModule }            from '@angular/platform-browser';
import { NgModule }                 from '@angular/core';
import { FormsModule }              from '@angular/forms';
import { HttpModule }               from '@angular/http';
import { RouterModule }             from '@angular/router';
import { AppRoutingModule }         from './app-routing.module';
import { NgProgressModule }         from 'ng2-progressbar';

import { AppComponent }             from './app.component';
import { AuthComponent }            from './components/auth/auth.component';
import { ErrorComponent }           from './components/error/error.component';
import { HeaderComponent }          from './components/header/header.component';
import { FooterComponent }          from './components/footer/footer.component';
import { SearchComponent }          from './components/search/search.component';
import { MarkdownComponent }        from './components/markdown/markdown.component';
import { SearchAddComponent }       from './components/search-add/search-add.component';
import { PaginationComponent }      from './components/pagination/pagination.component';
import { SearchResultComponent }    from './components/search-result/search-result.component';
import { SearchQuestionComponent }  from './components/search-question/search-question.component';
import { SearchQuestionsComponent } from './components/search-questions/search-questions.component';

import { AuthService }              from './services/auth.service';
import { ErrorService }             from './services/error.service';
import { SearchService }            from './services/search.service';
import { QuestionService }          from './services/question.service';



@NgModule({
  declarations: [
    AppComponent,
    SearchComponent,
    HeaderComponent,
    SearchResultComponent,
    SearchQuestionComponent,
    SearchAddComponent,
    MarkdownComponent,
    AuthComponent,
    FooterComponent,
    SearchQuestionsComponent,
    ErrorComponent,
    PaginationComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AppRoutingModule,
    NgProgressModule,
  ],
  providers: [
    AuthService,
    ErrorService,
    SearchService,
    QuestionService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
