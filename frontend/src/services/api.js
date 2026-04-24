import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://wcasumuwrsusqqmgouze.supabase.co';
const supabaseKey = 'sb_publishable_jTwXIQpfzIIyOOIKoOikBg_u8sEtVq8';
const supabase = createClient(supabaseUrl, supabaseKey);

export async function getEvents(from, to) {
    const pageSize = 1000;
    let all = [];
    let page = 0;
    while (true) {
        let query = supabase
            .from('events')
            .select('*')
            .order('year')
            .range(page * pageSize, page * pageSize + pageSize - 1);
        if (from && to) {
            query = query.gte('year', from).lte('year', to);
        }
        const { data, error } = await query;
        if (error) throw error;
        all = all.concat(data);
        if (data.length < pageSize) break;
        page++;
    }
    return all;
}

export async function getEventById(id) {
    const { data, error } = await supabase
        .from('events')
        .select('*')
        .eq('id', id)
        .single();
    
    if (error) throw error;
    return data;
}

export async function createUser(name, role) {
    const { data, error } = await supabase
        .from('users')
        .insert([{ name, role }])
        .select();
    
    if (error) throw error;
    return data[0];
}