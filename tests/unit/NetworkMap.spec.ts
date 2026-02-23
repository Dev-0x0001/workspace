import { describe, it, expect, beforeEach, vi, afterAll } from 'vitest';
import { mount } from '@cypress/vue';
import NetworkMap from '@/components/NetworkMap.vue';
import { createTestingPinia } from '@pinia/testing';
import { useNetworkStore } from '@/stores/network';

describe('NetworkMap', () => {
  let pinia: ReturnType<typeof createTestingPinia>;
  let networkStore: ReturnType<typeof useNetworkStore>;

  beforeEach(() => {
    pinia = createTestingPinia();
    networkStore = useNetworkStore();
    networkStore.$reset();
  });

  it('renders the network map', () => {
    const wrapper = mount(NetworkMap, {
      pinia,
      props: { 
        hosts: [],
        activeHost: null
      }
    });

    expect(wrapper).toBeTruthy();
    expect(wrapper.find('h2').text()).toBe('Network Map');
  });

  it('displays hosts', () => {
    const hosts = [
      { id: '1', ip: '192.168.1.1', mac: '00:11:22:33:44:55', name: 'Router', status: 'online' },
      { id: '2', ip: '192.168.1.2', mac: '00:11:22:33:44:56', name: 'Workstation', status: 'offline' }
    ];

    const wrapper = mount(NetworkMap, {
      pinia,
      props: { 
        hosts,
        activeHost: null
      }
    });

    expect(wrapper.findAll('.host-node')).toHaveLength(2);
    expect(wrapper.find(`.host-node[id=