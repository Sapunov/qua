import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SearchQuestionsComponent } from './components/search-questions/search-questions.component';
import { SearchResultComponent } from './components/search-result/search-result.component';
import { SearchQuestionComponent } from './components/search-question/search-question.component';
import { SearchAddComponent } from './components/search-add/search-add.component';
import { AuthComponent } from './components/auth/auth.component';

import { AuthService } from './services/auth.service';

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
  {
    path: 'add',
    component: SearchAddComponent,
    canActivate: [AuthService]
  },
  {
    path: 'edit',
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
