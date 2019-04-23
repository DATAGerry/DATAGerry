import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SearchRoutingModule } from './search-routing.module';
import { SearchComponent } from './search.component';
import {LayoutModule} from "../layout/layout.module";
import { TextSearchComponent } from './components/text-search/text-search.component';
import {ApiCallService} from "../services/api-call.service";

@NgModule({
  declarations: [SearchComponent, TextSearchComponent],
  imports: [
    CommonModule,
    LayoutModule,
    SearchRoutingModule
  ],

  providers: [ApiCallService]
})
export class SearchModule { }
