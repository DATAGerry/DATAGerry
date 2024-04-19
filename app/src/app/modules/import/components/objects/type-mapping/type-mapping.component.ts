/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
import {
    ChangeDetectorRef,
    Component,
    ComponentFactory,
    ComponentFactoryResolver,
    ComponentRef,
    EventEmitter,
    forwardRef,
    Input,
    OnChanges,
    OnDestroy,
    OnInit,
    Output,
    SimpleChanges,
    ViewChild,
    ViewContainerRef
} from '@angular/core';
import { UntypedFormControl, UntypedFormGroup, Validators } from '@angular/forms';

import { BehaviorSubject, Observable, Subscription } from 'rxjs';

import { TypeService } from '../../../../../framework/services/type.service';

import { CmdbType } from '../../../../../framework/models/cmdb-type';
import { JsonMappingComponent } from '../json-mapping/json-mapping.component';
import { CsvMappingComponent } from '../csv-mapping/csv-mapping.component';
import { TypeMappingBaseComponent } from './type-mapping-base.component';
import { AccessControlPermission } from 'src/app/modules/acl/acl.types';
/* ------------------------------------------------------------------------------------------------------------------ */

export const mappingComponents: { [type: string]: any } = {
    json: JsonMappingComponent,
    csv: CsvMappingComponent
};

@Component({
    selector: 'cmdb-type-mapping',
    templateUrl: './type-mapping.component.html',
    styleUrls: ['./type-mapping.component.scss'],
    providers: [{ provide: TypeMappingBaseComponent, useExisting: forwardRef(() => TypeMappingComponent) }]
})
export class TypeMappingComponent extends TypeMappingBaseComponent implements OnInit, OnChanges, OnDestroy {

    @ViewChild('mappingContainer', { read: ViewContainerRef, static: false }) mappingContainer;
    @Output() public typeChange: EventEmitter<any>;
    @Input() public fileFormat;
    @Input() public manuallyMapping: boolean = true;

    private readonly defaultMappingValues = [
        {
            name: 'public_id',
            label: 'Public ID',
            type: 'property'
        },
        {
            name: 'active',
            label: 'Active',
            type: 'property'
        }
    ];

    private typeListSubscription: Subscription;
    private valueChangeSubscription: Subscription;

    private typeIDSubject: BehaviorSubject<number>;
    public typeID: Observable<number>;
    private typeIDSubscription: Subscription;
    public typeList: CmdbType[];
    public typeInstance: CmdbType;
    public configForm: UntypedFormGroup;

    private component: any;
    public componentRef: ComponentRef<any>;
    private currentFactory: ComponentFactory<any>;


    public get currentTypeID(): number {
        return this.typeIDSubject.value;
    }

/* ------------------------------------------------------------------------------------------------------------------ */
/*                                                     LIFE CYCLE                                                     */
/* ------------------------------------------------------------------------------------------------------------------ */

    constructor(
        private typeService: TypeService,
        private ref: ChangeDetectorRef,
        private resolver: ComponentFactoryResolver
    ) {
        super();

        this.typeChange = new EventEmitter<any>();

        this.configForm = new UntypedFormGroup({
            typeID: new UntypedFormControl(null, Validators.required)
        });

        this.typeIDSubject = new BehaviorSubject<number>(null);
        this.typeID = this.typeIDSubject.asObservable();
        this.typeIDSubscription = new Subscription();
    }


    public ngOnInit(): void {
        this.typeListSubscription = this.typeService.getTypeList(
            [AccessControlPermission.READ, AccessControlPermission.CREATE, AccessControlPermission.UPDATE])
            .subscribe((typeList: CmdbType[]) => {
                this.typeList = typeList;

                if (typeList.length === 1) {
                    this.configForm.get('typeID').patchValue(this.typeList[0].public_id);
                }
            });

            this.valueChangeSubscription = this.configForm.get('typeID').valueChanges.subscribe((typeID: number) => {
                this.typeService.getType(+typeID).subscribe((typeInstance: CmdbType) => {
                    this.typeInstance = Object.assign(new CmdbType(), typeInstance) as CmdbType;
                    this.typeIDSubject.next(+typeID);
                    this.typeChange.emit({ typeID: this.currentTypeID, typeInstance: this.typeInstance });
                });
            });

            this.typeIDSubscription = this.typeID.subscribe((typeID: number) => {
                if (typeID !== null && typeID !== undefined) {
                    this.initMapping();
                }
            }
        );
    }


    public ngOnChanges(changes: SimpleChanges): void {
        if (changes.parsedData !== undefined &&
            changes.parsedData.currentValue !== undefined &&
            changes.parsedData.firstChange !== true) {
                this.initMapping();
        }
    }


    public ngOnDestroy(): void {
        this.typeListSubscription.unsubscribe();
        this.valueChangeSubscription.unsubscribe();
        this.typeIDSubscription.unsubscribe();
    }

/* ------------------------------------------------- HELPER METHODS ------------------------------------------------- */

    public initMapping() {
        this.currentMapping = [];
        this.mappingControls = [];

        for (const meta of this.defaultMappingValues) {
            this.mappingControls.push({
                name: meta.name,
                label: meta.label,
                type: 'property'
            });
        }

        if (this.typeInstance !== undefined) {
            for (const field of this.typeInstance.fields) {
                this.mappingControls.push({
                name: field.name,
                label: field.label,
                type: 'field'
                });
            }

            this.hasReferences = this.typeInstance.has_references();

            if (this.hasReferences) {
                const refFields = this.typeInstance.get_reference_fields();
                let workingRefType;

                for (const refField of refFields) {
                    workingRefType = this.typeList.find(id => id.public_id === refField.ref_types ||
                                     (Array.isArray(refField.ref_types) &&
                                     refField.ref_types.includes(id.public_id))) as CmdbType;

                    if (workingRefType) {
                        for (const typeField of workingRefType.fields) {
                            this.mappingControls.push({
                                name: refField.name,
                                ref_name: typeField.name,
                                label: typeField.label,
                                type: 'ref',
                                type_id: workingRefType.public_id,
                                type_name: workingRefType.name
                            });
                        }
                    }
                }
            }
        }

        this.loadMappingComponent();
    }


    private resetMappingComponent(): void {
        this.mappingContainer.clear();
        this.component = mappingComponents[this.fileFormat];
        this.currentFactory = this.resolver.resolveComponentFactory(this.component);
    }


    private loadMappingComponent(): void {
        this.resetMappingComponent();
        this.componentRef = this.mappingContainer.createComponent(this.currentFactory);
        this.componentRef.instance.parserConfig = this.parserConfig;
        this.componentRef.instance.parsedData = this.parsedData;
        this.componentRef.instance.mappingControls = this.mappingControls;
        this.componentRef.instance.currentMapping = this.currentMapping;
        this.componentRef.instance.mappingChange = this.mappingChange;
    }
}
