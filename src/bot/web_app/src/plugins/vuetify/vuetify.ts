import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import { createVuetify, type VuetifyOptions } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const config: VuetifyOptions = {
    components: { ...components },
    directives: { ...directives },
};

export default createVuetify(config);
