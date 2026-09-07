/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2026 becon GmbH
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
/* ------------------------------------------------------------------------------------------------------------------ */

/** ACL right guarding the port REST routes. */
export const PORT_VIEW_RIGHT = 'base.framework.port.view';

/** ACL right the create route is protected with. */
export const PORT_ADD_RIGHT = 'base.framework.port.add';

/**
 * Which face of its owner object a port sits on.
 *
 * FRONT/REAR are the two faces of a patch panel and only ever appear in pairs, SINGLE is an ordinary
 * device port. Panel-ness is read from this field alone - never from port names.
 */
export enum PortSide {
    SINGLE = 'single',
    FRONT = 'front',
    REAR = 'rear'
}


/**
 * A port as `GET /ports/object/<object_id>` returns it.
 *
 * The three option fields hold the `public_id` of a CmdbExtendableOption, not a label, so they have to
 * be resolved before they can be shown. `connected` is computed from the port's connections on read
 * and never stored, which is why it is optional here: an older backend simply omits it.
 */
export interface CmdbPort {
    public_id: number;
    object_id: number;
    side: PortSide;
    name: string;
    port_number: number | null;
    status: number | null;
    port_type: number | null;
    speed: number | null;
    description: string | null;
    author_id: number | null;
    creation_time: { $date: number } | null;
    last_edit_time: { $date: number } | null;
    connected?: boolean;
}


/** One table row: a port with its option ids resolved to the labels the user picked them by. */
export interface PortRow {
    publicId: number;
    name: string;
    side: PortSide;
    sideLabel: string;
    portNumber: number | null;
    status: string | null;
    portType: string | null;
    speed: string | null;
    description: string | null;
    connected: boolean;
}


/**
 * Body of `POST /ports/`. The option fields take an option's `public_id` or null, never a string.
 *
 * `side` is left out on purpose: front/rear is what the panel creation assistant sets, and the
 * route defaults a port to SINGLE.
 */
export interface PortCreatePayload {
    object_id: number;
    name: string;
    port_number: number | null;
    status: number | null;
    port_type: number | null;
    speed: number | null;
    description: string | null;
}
