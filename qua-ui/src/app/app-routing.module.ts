import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SearchQuestionsComponent } from './search-questions/search-questions.component';
// import { SearchCategoryComponent } from './search-category/search-category.component';
import { SearchResultComponent } from './search-result/search-result.component';
import { SearchQuestionComponent } from './search-question/search-question.component';
import { SearchAddComponent } from './search-add/search-add.component';
import { AuthComponent } from './auth/auth.component';

import { AuthService } from './auth.service';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/search',
    pathMatch: 'full'
  },
  {
    path: 'search',
    component: SearchResultComponent,
    canActivate: [AuthService]
  },
  {
    path: 'questions',
    component: SearchQuestionsComponent,
    canActivate: [AuthService]
  },
  {
    path: 'questions/:id',
    component: SearchQuestionComponent,
    canActivate: [AuthService]
  },
  // {
  //   path: 'category',
  //   component: SearchCategoryComponent,
  //   canActivate: [AuthService]
  // },
  {
    path: 'add',
    component: SearchAddComponent,
    canActivate: [AuthService]
  },
  {
    path: 'auth',
    component: AuthComponent
  },
  {
    path: '**',
    redirectTo: '/search',
    pathMatch: 'full'
  },
];
@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
