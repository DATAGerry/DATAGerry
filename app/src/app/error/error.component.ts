/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import {
  Component,
  ComponentFactory,
  ComponentFactoryResolver, ComponentRef,
  OnDestroy,
  OnInit,
  ViewChild,
  ViewContainerRef
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PreviousRouteService } from '../services/previous-route.service';
import { Subscription } from 'rxjs';
import { errorComponents } from './error.list';

@Component({
  templateUrl: './error.component.html',
  styleUrls: ['./error.component.scss']
})
export class ErrorComponent implements OnInit, OnDestroy {

  @ViewChild('errorContainer', { read: ViewContainerRef, static: true }) public errorContainer;
  private componentRef: ComponentRef<any>;

  public previousUrl: string;

  private statusCodeSubscription: Subscription;
  private readonly defaultStatusCode: number = 404;
  public statusCode: number = this.defaultStatusCode;


  constructor(private route: ActivatedRoute, private resolver: ComponentFactoryResolver,
              private prevRouteService: PreviousRouteService) {
    this.statusCodeSubscription = this.route.params.subscribe(params => this.statusCode = params.statusCode);
  }

  public ngOnInit(): void {
    this.createErrorComponent(this.statusCode);
    this.previousUrl = this.prevRouteService.getPreviousUrl();
  }

  private createErrorComponent(statusCode: number) {
    const factory: ComponentFactory<any> = this.resolver.resolveComponentFactory(errorComponents[statusCode]);
    this.componentRef = this.errorContainer.createComponent(factory);
  }

  public ngOnDestroy(): void {
    this.errorContainer.clear();
    this.componentRef.destroy();
    this.statusCodeSubscription.unsubscribe();
  }

}
