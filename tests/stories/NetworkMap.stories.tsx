import { NetworkMap } from '@/components/NetworkMap.vue';
import { Host } from '@/types/host';

export default {
  title: 'components/NetworkMap',
  component: NetworkMap,
  argTypes: {
    hosts: { control: 'array' },
    activeHost: { control: 'object' }
  }
};

const Template = (args) => ({
  components: { NetworkMap },
  template: '<NetworkMap :hosts="args.hosts" :active-host="args.activeHost" />'
});

export const Default = Template.bind({});
Default.args = {
  hosts: [],
  activeHost: null
};

export const WithHosts = Template.bind({});
WithHosts.args = {
  hosts: [
    { id: '1', ip: '192.168.1.1', mac: '00:11:22:33:44:55', name: 'Router', status: 'online' }
  ],
  activeHost: null
};