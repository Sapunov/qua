// import { InMemoryWebApiModule }    from 'angular-in-memory-web-api';
// import { InMemoryDataService }     from './in-memory-data.service';

import { BrowserModule }           from '@angular/platform-browser';
import { NgModule }                from '@angular/core';
import { FormsModule }             from '@angular/forms';
import { HttpModule }              from '@angular/http';
import { RouterModule }            from '@angular/router';
import { AppRoutingModule }        from './app-routing.module';

import { AppComponent }            from './app.component';
import { AuthComponent }           from './auth/auth.component';
import { HeaderComponent }         from './header/header.component';
import { FooterComponent }         from './footer/footer.component';
import { SearchComponent }         from './search/search.component';
import { MarkdownComponent }       from './markdown/markdown.component';
import { SearchAddComponent }      from './search-add/search-add.component';
import { SearchResultComponent }   from './search-result/search-result.component';
import { SearchQuestionComponent } from './search-question/search-question.component';

import { AuthService }             from './auth.service';
import { ErrorService }            from './error.service';
import { SearchService }           from './search.service';
import { QuestionService }         from './question.service';
import { CategoryService }         from './category.service';
import { SearchCategoryComponent } from './search-category/search-category.component';



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
    SearchCategoryComponent
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
