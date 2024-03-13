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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { CmdbDao } from './cmdb-dao';
import { AccessControlList } from '../../acl/acl.types';
/* ------------------------------------------------------------------------------------------------------------------ */

export interface CmdbTypeSection {
    type: string;
    name: string;
    label: string;
    fields?: Array<any>;
    reference?: {
        type_id: number;
        section_name: string;
        selected_fields?: Array<string>;
    };
}


export interface CmdbTypeExternalLink {
    name: string;
    href: string;
    label: string;
    icon: string;
    fields: Array<any>;
}


export interface CmdbTypeMeta {
    icon: string;
    sections: Array<CmdbTypeSection>;
    externals: Array<CmdbTypeExternalLink>;
    summary: CmdbTypeSummary;
}


export interface CmdbTypeSummary {
    fields: Array<string>;
}


export class CmdbType implements CmdbDao {
    public readonly public_id: number;
    public name: string;
    public label?: string;
    public description?: string;
    public active: boolean;
    public selectable_as_parent: boolean;
    public global_template_ids?: Array<string> = [];
    public author_id: number;
    public version: string;
    public creation_time: any;
    public editor_id: number;
    public last_edit_time: any;
    public render_meta: CmdbTypeMeta;
    public fields: Array<any> = [];
    public acl?: AccessControlList;


    public has_references(): boolean {
        for (const field of this.fields) {
            if (field.type === 'ref') {
                return true;
            }
        }

        return false;
    }


    public get_reference_fields() {
        const refFields = [];

        for (const field of this.fields) {
            if (field.type === 'ref') {
                refFields.push(field);
            }
        }

        return refFields;
    }
}
