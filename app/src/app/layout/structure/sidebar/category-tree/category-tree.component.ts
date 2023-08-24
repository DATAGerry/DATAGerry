/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
import { Component, OnInit } from '@angular/core';
import {NestedTreeControl} from '@angular/cdk/tree';
import {MatTreeNestedDataSource } from '@angular/material/tree';
import { LocationService } from 'src/app/framework/services/location.service';
import { CollectionParameters } from 'src/app/services/models/api-parameter';
import { RenderResult } from '../../../../framework/models/cmdb-render';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from 'src/app/services/models/api-response';
import { ReplaySubject, BehaviorSubject } from 'rxjs';
import { Router } from '@angular/router';
import * as internal from 'stream';

interface LocationNode {
    name: string;
    icon: string;
    parent: number;
    object_id: number;
    children?: LocationNode[];
  }
  
  // const TREE_DATA: LocationNode[] = [
  //   {
  //     name: 'Fruit',
  //     icon: 'fas fa-server',
  //     object_id: 1,
  //     children: [{name: 'Apple', icon: 'fas fa-globe', object_id: 5}, {name: 'Banana', icon: 'fas fa-globe',  object_id: 6}, {name: 'Fruit loops', icon: 'fas fa-globe',  object_id: 11}],
  //   },
  //   {
  //     name: 'Vegetables',
  //     icon: 'fas fa-server',
  //     object_id: 2,
  //     children: [
  //       {
  //         name: 'Green',
  //         object_id: 3,
  //         icon: 'fas fa-server',
  //         children: [{name: 'Broccoli',  object_id: 7, icon: 'fas fa-globe'}, {name: 'Brussels sprouts',  object_id: 9, icon: 'fas fa-globe'}],
  //       },
  //       {
  //         name: 'Orange',
  //         object_id: 4,
  //         icon: 'fas fa-server',
  //         children: [{name: 'Pumpkins',  object_id: 8, icon: 'fas fa-globe'}, {name: 'Carrots', object_id: 10, icon: 'fas fa-globe'}],
  //       },
  //     ],
  //   },
  // ];

@Component({
    selector: 'category-tree',
    templateUrl: './category-tree.component.html',
    styleUrls: ['./category-tree.component.scss'],
})
export class CategoryTreeComponent implements OnInit {

    private unsubscribe: ReplaySubject<void> = new ReplaySubject<void>();
    public changedReference: BehaviorSubject<any> = new BehaviorSubject<any>(undefined);

    treeControl = new NestedTreeControl<LocationNode>(node => node.children);
    dataSource = new MatTreeNestedDataSource<LocationNode>();

    //used for highlighting the selected location
    private selectedLocationID: number;
    //used as data source
    locationsList: RenderResult[];  

    


/* -------------------------------------------------------------------------- */
/*                                LIFE - CYCLE                                */
/* -------------------------------------------------------------------------- */


    constructor(private locationService: LocationService, private route: Router){
        // this.dataSource.data = TREE_DATA;
    }

    public ngOnInit(){
        this.getLocationTree();
    }

    /* -------------------------------------------------------------------------- */
    /*                             HELPER - FUNCTIONS                             */
    /* -------------------------------------------------------------------------- */

    /**
     * Get all locations except the root location
     */
    private getLocationTree(){
        const params: CollectionParameters = {
          filter: [{ $match: { public_id: { $gt: 1 } } }],
          limit: 0, sort: 'public_id', order: 1, page: 1
        };
    
        this.locationService.getLocationsTree(params).pipe(takeUntil(this.unsubscribe))
              .subscribe((apiResponse: APIGetMultiResponse<RenderResult>) => {
                this.locationsList = apiResponse.results;
                console.log("locationSList: ", this.locationsList);

                this.dataSource.data = this.forceCast<LocationNode[]>(this.locationsList);

                for(var location in this.locationsList){
                  console.log("Location:", location);
                }
        });
    }

    /**
     * Set the selected location and loads the object overview in the content view
     * 
     * @param clickedObjectID the objectID of the location which is clicked in location tree
     */
    private locationClicked(clickedObjectID: number){
      this.selectedLocationID = clickedObjectID;
      this.route.navigateByUrl('/framework/object/view/'+clickedObjectID);
      
    }

    /**
     * TreeControl function
     */
    hasChild = (_: number, node: LocationNode) => !!node.children && node.children.length > 0;

    public forceCast<T>(input: any): T {

      // ... do runtime checks here
    
      // @ts-ignore <-- forces TS compiler to compile this as-is
      return input;
    }
}