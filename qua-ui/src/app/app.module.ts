// import { InMemoryWebApiModule }    from 'angular-in-memory-web-api';
// import { InMemoryDataService }     from './in-memory-data.service';

import { BrowserModule }            from '@angular/platform-browser';
import { NgModule }                 from '@angular/core';
import { FormsModule }              from '@angular/forms';
import { HttpModule }               from '@angular/http';
import { RouterModule }             from '@angular/router';
import { AppRoutingModule }         from './app-routing.module';

import { AppComponent }             from './app.component';
import { AuthComponent }            from './auth/auth.component';
import { HeaderComponent }          from './header/header.component';
import { FooterComponent }          from './footer/footer.component';
import { SearchComponent }          from './search/search.component';
import { MarkdownComponent }        from './markdown/markdown.component';
import { SearchAddComponent }       from './search-add/search-add.component';
import { SearchResultComponent }    from './search-result/search-result.component';
import { SearchQuestionComponent }  from './search-question/search-question.component';
// import { SearchCategoryComponent }  from './search-category/search-category.component';
import { SearchQuestionsComponent } from './search-questions/search-questions.component';

import { AuthService }              from './services/auth.service';
import { ErrorService }             from './services/error.service';
import { SearchService }            from './services/search.service';
import { QuestionService }          from './services/question.service';
import { CategoryService }          from './services/category.service';



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
    // SearchCategoryComponent,
    SearchQuestionsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AppRoutingModule
    // InMemoryWebApiModule.forRoot(InMemoryDataService)
  ],
  providers: [
    AuthService,
    ErrorService,
    SearchService,
    CategoryService,
    QuestionService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
