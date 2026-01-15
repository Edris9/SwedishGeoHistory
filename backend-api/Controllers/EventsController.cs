using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using backend_api.Data;
using backend_api.Models;

namespace backend_api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class EventsController : ControllerBase
{
    private readonly AppDbContext _context;

    public EventsController(AppDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<Event>>> GetEvents(int? from, int? to)
    {
        var query = _context.Events.AsQueryable();

        if (from.HasValue)
            query = query.Where(e => e.Year >= from.Value);
        if (to.HasValue)
            query = query.Where(e => e.Year <= to.Value);

        return await query.OrderBy(e => e.Year).ToListAsync();
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Event>> GetEvent(int id)
    {
        var evt = await _context.Events.FindAsync(id);
        if (evt == null) return NotFound();
        return evt;
    }
}