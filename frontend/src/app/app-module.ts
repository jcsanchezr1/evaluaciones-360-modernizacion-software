import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing-module';
import { App } from './app';
import { Sidebar } from './layout/sidebar/sidebar';
import { Header } from './layout/header/header';
import { Evaluations } from './evaluations/evaluations';
import { provideHttpClient } from '@angular/common/http';

@NgModule({
  declarations: [
    App,
    Sidebar,
    Header,
    Evaluations
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [
    provideHttpClient(),
    provideBrowserGlobalErrorListeners()
  ],
  bootstrap: [App]
})
export class AppModule { }